from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from sqlalchemy import desc

from applications.common import curd
from applications.common.curd import enable_status, disable_status
from applications.common.utils.http import table_api, fail_api, success_api
from applications.common.utils.rights import authorize
from applications.common.utils.validate import str_escape
from applications.extensions import db
from applications.models import Role, Dept
from applications.models import User, AdminLog

bp = Blueprint('user', __name__, url_prefix='/user')


# 用户管理
@bp.get('/')
@authorize("system:user:main")
def main():
    return render_template('system/user/main.html')


#   用户分页查询
@bp.get('/data')
@authorize("system:user:main")
def data():
    # 获取请求参数
    real_name = str_escape(request.args.get('realname', type=str))

    username = str_escape(request.args.get('username', type=str))
    dept_id = request.args.get('deptId', type=int)

    filters = []
    if real_name:
        filters.append(User.realname.contains(real_name))
    if username:
        filters.append(User.username.contains(username))
    if dept_id:
        filters.append(User.dept_id == dept_id)

    # print(*filters)
    query = db.session.query(
        User,
        Dept
    ).filter(*filters).outerjoin(Dept, User.dept_id == Dept.id).layui_paginate()

    return table_api(
        data=[{
            'id': user.id,
            'username': user.username,
            'realname': user.realname,
            'enable': user.enable,
            'create_at': user.create_at,
            'update_at': user.update_at,
            'dept_name': dept.dept_name if dept else None
        } for user, dept in query.items],
        count=query.total)

    # 用户增加


@bp.get('/add')
@authorize("system:user:add", log=True)
def add():
    roles = Role.query.all()
    return render_template('system/user/add.html', roles=roles)


@bp.post('/save')
@authorize("system:user:add", log=True)
def save():
    req_json = request.get_json(force=True)
    a = req_json.get("roleIds")
    username = str_escape(req_json.get('username'))
    real_name = str_escape(req_json.get('realName'))
    password = str_escape(req_json.get('password'))
    role_ids = a.split(',')

    if not username or not real_name or not password:
        return fail_api(msg="账号姓名密码不得为空")

    if bool(User.query.filter_by(username=username).count()):
        return fail_api(msg="用户已经存在")

    user = User(username=username, realname=real_name, enable=1)
    user.set_password(password)
    db.session.add(user)
    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    for r in roles:
        user.role.append(r)
    db.session.commit()

    return success_api(msg="增加成功")


# 删除用户
@bp.delete('/remove/<int:id>')
@authorize("system:user:remove", log=True)
def delete(id):
    user = User.query.filter_by(id=id).first()
    user.role = []

    res = User.query.filter_by(id=id).delete()
    db.session.commit()
    if not res:
        return fail_api(msg="删除失败")
    return success_api(msg="删除成功")


#  编辑用户
@bp.get('/edit/<int:id>')
@authorize("system:user:edit", log=True)
def edit(id):
    user = curd.get_one_by_id(User, id)
    roles = Role.query.all()
    checked_roles = []
    for r in user.role:
        checked_roles.append(r.id)
    return render_template('system/user/edit.html', user=user, roles=roles, checked_roles=checked_roles)


#  编辑用户
@bp.put('/update')
@authorize("system:user:edit", log=True)
def update():
    req_json = request.get_json(force=True)
    a = str_escape(req_json.get("roleIds"))
    id = str_escape(req_json.get("userId"))
    username = str_escape(req_json.get('username'))
    real_name = str_escape(req_json.get('realName'))
    dept_id = str_escape(req_json.get('deptId'))
    role_ids = a.split(',')
    User.query.filter_by(id=id).update({'username': username, 'realname': real_name, 'dept_id': dept_id})
    u = User.query.filter_by(id=id).first()

    roles = Role.query.filter(Role.id.in_(role_ids)).all()
    u.role = roles

    db.session.commit()
    return success_api(msg="更新成功")


# 个人中心
@bp.get('/center')
@login_required
def center():
    user_info = current_user
    user_logs = AdminLog.query.filter_by(url='/passport/login').filter_by(uid=current_user.id).order_by(
        desc(AdminLog.create_time)).limit(10)
    return render_template('system/user/center.html', user_info=user_info, user_logs=user_logs)


# 修改头像
@bp.get('/profile')
@login_required
def profile():
    return render_template('system/user/profile.html')


# 修改头像
@bp.put('/updateAvatar')
@login_required
def update_avatar():
    url = request.get_json(force=True).get("avatar").get("src")
    r = User.query.filter_by(id=current_user.id).update({"avatar": url})
    db.session.commit()
    if not r:
        return fail_api(msg="出错啦")
    return success_api(msg="修改成功")


# 修改当前用户信息
@bp.put('/updateInfo')
@login_required
def update_info():
    req_json = request.get_json(force=True)
    r = User.query.filter_by(id=current_user.id).update(
        {"realname": req_json.get("realName"), "remark": req_json.get("details")})
    db.session.commit()
    if not r:
        return fail_api(msg="出错啦")
    return success_api(msg="更新成功")


# 修改当前用户密码
@bp.get('/editPassword')
@login_required
def edit_password():
    return render_template('system/user/edit_password.html')


# 修改当前用户密码
@bp.put('/editPassword')
@login_required
def edit_password_put():
    res_json = request.get_json(force=True)
    if res_json.get("newPassword") == '':
        return fail_api("新密码不得为空")
    if res_json.get("newPassword") != res_json.get("confirmPassword"):
        return fail_api("俩次密码不一样")
    user = current_user
    is_right = user.validate_password(res_json.get("oldPassword"))
    if not is_right:
        return fail_api("旧密码错误")
    user.set_password(res_json.get("newPassword"))
    db.session.add(user)
    db.session.commit()
    return success_api("更改成功")


# 启用用户
@bp.put('/enable')
@authorize("system:user:edit", log=True)
def enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = enable_status(model=User, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="启动成功")
    return fail_api(msg="数据错误")


# 禁用用户
@bp.put('/disable')
@authorize("system:user:edit", log=True)
def dis_enable():
    _id = request.get_json(force=True).get('userId')
    if _id:
        res = disable_status(model=User, id=_id)
        if not res:
            return fail_api(msg="出错啦")
        return success_api(msg="禁用成功")
    return fail_api(msg="数据错误")
