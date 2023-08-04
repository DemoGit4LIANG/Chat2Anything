import os
import shutil
import time

from flask import Blueprint, request, render_template, jsonify, current_app
from flask_login import current_user
from sqlalchemy import desc

from applications.common.curd import model_to_dicts
from applications.common.utils.http import fail_api, success_api, table_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import KnowledgeStore, User, Dept
from applications.schemas.knowledge_store import KnowledgeStoreOutSchema
from chains.local_vector_stroe import LocalVectorStore
from configs.model_config import VECTOR_ROOT_PATH

from applications.common.utils.logger import *

bp = Blueprint('knowledge_store', __name__, url_prefix='/store')


# 知识库管理
@bp.get('/')
@authorize("knowledge:store:main")
def index():
    return render_template('knowledge/store.html')


# 拉取知识库数据
@bp.get('/table')
@authorize("knowledge:store:main")
def table():
    page = request.args.get('page', type=int)
    limit = request.args.get('limit', type=int)
    data, count = _get_knowledge_store(page, limit)

    return table_api(data=data, count=count)


@bp.route('/delete', methods=['GET', 'POST'])
@authorize("knowledge:store:delete", log=True)
def delete():
    _id = request.form.get('id')
    del_store = KnowledgeStore.query.filter_by(id=_id).first()
    if not del_store:
        logger.info(f"{del_store.name} fail to delete")
        return fail_api(msg="删除失败, 请刷新后重新尝试")
    db.session.delete(del_store)
    db.session.commit()
    if del_store:
        shutil.rmtree(del_store.path)
        logger.info(f"vector store {del_store.name} has been deleted")
        return success_api(msg="删除成功")
    else:
        logger.info(f"vector store {del_store.name} fail to delete")
        return fail_api(msg="删除失败")


# 批量删除
@bp.route('/batchRemove', methods=['GET', 'POST'])
@authorize("knowledge:store:delete", log=True)
def batch_remove():
    ids = request.form.getlist('ids[]')
    dels = KnowledgeStore.query.filter(KnowledgeStore.id.in_(ids)).all()
    fails = []
    for d in dels:
        try:
            shutil.rmtree(d.path)
            logger.info(f"向量库 {d.name} 文件已被删除")
            db.session.delete(d)
            db.session.commit()
        except:
            fails += d.name

    return success_api(msg="删除成功") if len(fails) == 0 else fail_api(msg=f"删除失败{fails}")

# 上传
@bp.get('/upload')
@authorize("knowledge:store:add", log=True)
def upload():
    return render_template('knowledge/store_add.html')


# 上传接口
@bp.post('/upload')
@authorize("knowledge:store:add", log=True)
def upload_api():

    timestamp = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())

    print(current_user.dept_id)

    vector_store_name = str_escape(request.values.get("input_name", type=str))
    vector_store_desc = str_escape(request.values.get("input_desc", type=str))

    if vector_store_name == "":
        return fail_api(msg="知识库名不能为空")

    if vector_store_desc == "":
        return fail_api(msg="知识库描述不能为空")

    if len(db.session.query(KnowledgeStore).filter_by(name=vector_store_name).all()) > 0:
        return fail_api(msg="知识库名已存在")

    uploaded_files = request.files.getlist("file")
    if len(uploaded_files) == 0:
        return fail_api(msg="未上传文件")

    dst_dir_path = os.path.join(VECTOR_ROOT_PATH, vector_store_name)

    store = KnowledgeStore(name=vector_store_name, create_user_id=current_user.id, create_dept_id=current_user.dept_id,
                           size=0., create_time=timestamp, update_time=timestamp,
                           desc=vector_store_desc, path=dst_dir_path)
    db.session.add(store)
    db.session.commit()

    if os.path.exists(dst_dir_path):
        shutil.rmtree(dst_dir_path)
    os.makedirs(dst_dir_path)

    file_list = []
    for file in uploaded_files:
        dst_file_path = os.path.join(dst_dir_path, file.filename)
        file.save(dst_file_path)
        file_list.append(dst_file_path)

    # TODO: wait optimization
    local_vector_store = LocalVectorStore()
    local_vector_store.init_cfg()

    # start to vectorize the docs
    _, success_files = local_vector_store.init_vector_store(file_list, dst_dir_path)
    fail_files = [os.path.split(f)[-1] for f in (set(file_list) - set(success_files))]
    msg, success_tag = ("上传成功", True) if len(fail_files) == 0 else (f"文件{fail_files}处理失败, 知识库创建失败", False)

    if not success_tag:
        shutil.rmtree(dst_dir_path)
        db.session.delete(store)
        logger.info(f"{dst_dir_path}已删除, 由于文件{fail_files}向量化失败")
    else:
        file_size = os.path.getsize(os.path.join(dst_dir_path, "index.faiss"))
        store.size = round(file_size/(1024*1024), 3)
        db.session.add(store)
        db.session.commit()

    res = {
        "msg": msg,
        "code": 0,
        "success": success_tag,
    }

    return jsonify(res)


def _get_knowledge_store(page, limit):
    knowledge_store = KnowledgeStore.query.order_by(desc(KnowledgeStore.create_time)).paginate(page=page, per_page=limit, error_out=False)
    count = KnowledgeStore.query.count()

    data = model_to_dicts(schema=KnowledgeStoreOutSchema, data=knowledge_store.items)
    for item in data:
        item["size"] = f"{item['size']} MB"
        create_user = db.session.get(User, item["create_user_id"])
        create_dept = db.session.get(Dept, item["create_dept_id"])
        item["create_user_name"] = create_user.username if create_user else "--"
        item["create_dept_name"] = create_dept.dept_name if create_dept else "--"

    return data, count