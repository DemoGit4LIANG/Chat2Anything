from flask import Flask

from applications.extensions.init_sqlalchemy import db
from flask_migrate import Migrate
from applications.models import *

migrate = Migrate()


def init_migrate(app: Flask):
    migrate.init_app(app, db)
