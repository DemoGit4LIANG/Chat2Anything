from functools import wraps
from flask import abort, request, jsonify, session, current_app
from flask_login import login_required, current_user
from applications.common.admin_log import admin_log


def authorize(power: str, log: bool = False):
    """用户权限判断，用于判断目前会话用户是否拥有访问权限

    :param power: 权限标识
    :type power: str
    :param log: 是否记录日志, defaults to False
    :type log: bool, optional
    """
    def decorator(func):
        @login_required
        @wraps(func)
        def wrapper(*args, **kwargs):
            # 定义管理员的id为1
            if current_user.username == current_app.config.get("SUPERADMIN"):
                return func(*args, **kwargs)
            if not power in session.get('permissions'):
                if log:
                    admin_log(request=request, is_access=False)
                if request.method == 'GET':
                    abort(403)
                else:
                    return jsonify(success=False, msg="权限不足!")
            if log:
                admin_log(request=request, is_access=True)
            return func(*args, **kwargs)

        return wrapper

    return decorator
