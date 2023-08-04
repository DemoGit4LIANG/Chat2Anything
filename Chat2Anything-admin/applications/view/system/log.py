from flask import Blueprint, request, render_template
from sqlalchemy import desc
from applications.common.utils.http import table_api
from applications.common.utils.rights import authorize
from applications.models import AdminLog
from applications.schemas import LogOutSchema
from applications.common.curd import model_to_dicts

bp = Blueprint('log', __name__, url_prefix='/log')


# 日志管理
@bp.get('/')
@authorize("system:log:main")
def index():
    return render_template('system/admin_log/main.html')


# 登录日志
@bp.get('/loginLog')
@authorize("system:log:main")
def login_log():
    # orm查询
    # 使用分页获取data需要.items
    log = AdminLog.query.filter_by(url='/passport/login').order_by(desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data= model_to_dicts(schema=LogOutSchema, data=log.items), count=count)


# 操作日志
@bp.get('/operateLog')
@authorize("system:log:main")
def operate_log():
    # orm查询
    # 使用分页获取data需要.items
    log = AdminLog.query.filter(
        AdminLog.url != '/passport/login').order_by(
        desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)
