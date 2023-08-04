from flask import session, current_app
from flask_login import current_user


def init_template_directives(app):
    @app.template_global()
    def authorize(power):
        if current_user.username != current_app.config.get("SUPERADMIN"):
            return bool(power in session.get('permissions'))
        else:
            return True
