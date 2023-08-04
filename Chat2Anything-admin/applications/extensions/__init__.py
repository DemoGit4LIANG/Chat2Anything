from flask import Flask

from .init_sqlalchemy import db, ma, init_databases
from .init_login import init_login_manager
from .init_template_directives import init_template_directives
from .init_error_views import init_error_views
from .init_mail import init_mail, mail as flask_mail
from .init_upload import init_upload
from .init_migrate import init_migrate


def init_plugs(app: Flask) -> None:
    init_login_manager(app)
    init_databases(app)
    init_template_directives(app)
    init_error_views(app)
    init_mail(app)
    init_upload(app)
    init_migrate(app)