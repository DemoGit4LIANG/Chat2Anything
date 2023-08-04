from flask import Blueprint, render_template, request, jsonify

from applications.common import curd
from applications.common.utils import validate
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Dept, User
from applications.schemas import DeptSchema

bp = Blueprint('dept', __name__, url_prefix='/dept')


@bp.get('/')
@authorize("system:dept:main", log=True)
def main():
    return render_template('system/dept/main.html')


@bp.post('/data')
@authorize("system:dept:main", log=True)
def data():
    data = Dept.query.order_by(Dept.sort).all()
    res = {
        "data": DeptSchema(many=True).dump(data)
    }
    return jsonify(res)


@bp.get('/add')
@authorize("system:dept:add", log=True)
def add():
    return render_template('system/dept/add.html')


@bp.get('/tree')
@authorize("system:dept:main", log=True)
def tree():
    dept = Dept.query.order_by(Dept.sort).all()
    power_data = curd.model_to_dicts(schema=DeptSchema, data=dept)
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": power_data

    }
    return jsonify(res)


@bp.post('/save')
@authorize("system:dept:add", log=True)
def save():
    req_json = request.get_json(force=True)
    dept = Dept(
        parent_id=req_json.get('parentId'),
        dept_name=str_escape(req_json.get('deptName')),
        sort=str_escape(req_json.get('sort')),
        leader=str_escape(req_json.get('leader')),
        phone=str_escape(req_json.get('phone')),
        email=str_escape(req_json.get('email')),
        status=str_escape(req_json.get('status')),
        address=str_escape(req_json.get('address'))
    )
    r = db.session.add(dept)
    db.session.commit()
    return success_api(msg="成功")


@bp.get('/edit')
@authorize("system:dept:edit", log=True)
def edit():
    _id = request.args.get("deptId")
    dept = curd.get_one_by_id(model=Dept, id=_id)
    return render_template('system/dept/edit.html', dept=dept)


# 启用
@bp.put('/enable')
@authorize("system:dept:edit", log=True)
def enable():
    id = request.get_json(force=True).get('deptId')
    if id:
        enable = 1
        d = Dept.query.filter_by(id=id).update({"status": enable})
        if d:
            db.session.commit()
            return success_api(msg="启用成功")
        return fail_api(msg="出错啦")
    return fail_api(msg="数据错误")


# 禁用
@bp.put('/disable')
@authorize("system:dept:edit", log=True)
def dis_enable():
    id = request.get_json(force=True).get('deptId')
    if id:
        enable = 0
        d = Dept.query.filter_by(id=id).update({"status": enable})
        if d:
            db.session.commit()
            return success_api(msg="禁用成功")
        return fail_api(msg="出错啦")
    return fail_api(msg="数据错误")


@bp.put('/update')
@authorize("system:dept:edit", log=True)
def update():
    json = request.get_json(force=True)
    id = json.get("deptId"),
    data = {
        "dept_name": validate.str_escape(json.get("deptName")),
        "sort": validate.str_escape(json.get("sort")),
        "leader": validate.str_escape(json.get("leader")),
        "phone": validate.str_escape(json.get("phone")),
        "email": validate.str_escape(json.get("email")),
        "status": validate.str_escape(json.get("status")),
        "address": validate.str_escape(json.get("address"))
    }
    d = Dept.query.filter_by(id=id).update(data)
    if not d:
        return fail_api(msg="更新失败")
    db.session.commit()
    return success_api(msg="更新成功")


@bp.delete('/remove/<int:_id>')
@authorize("system:dept:remove", log=True)
def remove(_id):
    d = Dept.query.filter_by(id=_id).delete()
    if not d:
        return fail_api(msg="删除失败")
    res = User.query.filter_by(dept_id=_id).update({"dept_id": None})
    db.session.commit()
    if res:
        return success_api(msg="删除成功")
    else:
        return fail_api(msg="删除失败")
