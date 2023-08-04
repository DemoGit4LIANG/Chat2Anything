from flask import Blueprint, render_template, request, jsonify

from applications.common import curd
from applications.common.utils.http import success_api, fail_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Power
from applications.schemas import PowerOutSchema2
from applications.schemas.admin_power import PowerSchema

bp = Blueprint('power', __name__, url_prefix='/power')


@bp.get('/')
@authorize("system:power:main")
def index():
    return render_template('system/power/main.html')


@bp.post('/data')
@authorize("system:power:main")
def data():
    power = Power.query.all()
    res = {
        "data": PowerSchema(many=True).dump(power)
    }
    return jsonify(res)


@bp.get('/add')
@authorize("system:power:add", log=True)
def add():
    return render_template('system/power/add.html')


@bp.get('/selectParent')
@authorize("system:power:main", log=True)
def select_parent():
    power = Power.query.all()
    res = curd.model_to_dicts(schema=PowerOutSchema2, data=power)
    res.append({"powerId": 0, "powerName": "顶级权限", "parentId": -1})
    res = {
        "status": {"code": 200, "message": "默认"},
        "data": res

    }
    return jsonify(res)


# 增加
@bp.post('/save')
@authorize("system:power:add", log=True)
def save():
    req = request.get_json(force=True)
    icon = str_escape(req.get("icon"))
    openType = str_escape(req.get("openType"))
    parentId = str_escape(req.get("parentId"))
    powerCode = str_escape(req.get("powerCode"))
    powerName = str_escape(req.get("powerName"))
    powerType = str_escape(req.get("powerType"))
    powerUrl = str_escape(req.get("powerUrl"))
    sort = str_escape(req.get("sort"))
    power = Power(
        icon=icon,
        open_type=openType,
        parent_id=parentId,
        code=powerCode,
        name=powerName,
        type=powerType,
        url=powerUrl,
        sort=sort,
        enable=1
    )
    r = db.session.add(power)
    db.session.commit()
    return success_api(msg="成功")


# 权限编辑
@bp.get('/edit/<int:_id>')
@authorize("system:power:edit", log=True)
def edit(_id):
    power = curd.get_one_by_id(Power, _id)
    icon = str(power.icon).split()
    if len(icon) == 2:
        icon = icon[1]
    else:
        icon = None
    return render_template('system/power/edit.html', power=power, icon=icon)


# 权限更新
@bp.put('/update')
@authorize("system:power:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    id = request.get_json(force=True).get("powerId")
    data = {
        "icon": str_escape(req_json.get("icon")),
        "open_type": str_escape(req_json.get("openType")),
        "parent_id": str_escape(req_json.get("parentId")),
        "code": str_escape(req_json.get("powerCode")),
        "name": str_escape(req_json.get("powerName")),
        "type": str_escape(req_json.get("powerType")),
        "url": str_escape(req_json.get("powerUrl")),
        "sort": str_escape(req_json.get("sort"))
    }
    res = Power.query.filter_by(id=id).update(data)
    db.session.commit()
    if not res:
        return fail_api(msg="更新权限失败")
    return success_api(msg="更新权限成功")


# 启用权限
@bp.put('/enable')
@authorize("system:power:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('powerId')
    if id:
        res = curd.enable_status(Power, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启用成功")
    return fail_api(msg="数据错误")


# 禁用权限
@bp.put('/disable')
@authorize("system:power:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('powerId')
    if id:
        res = curd.disable_status(Power, _id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")


# 权限删除
@bp.delete('/remove/<int:id>')
@authorize("system:power:remove", log=True)
def remove(id):
    power = Power.query.filter_by(id=id).first()
    power.role = []

    r = Power.query.filter_by(id=id).delete()
    db.session.commit()
    if r:
        return success_api(msg="删除成功")
    else:
        return fail_api(msg="删除失败")