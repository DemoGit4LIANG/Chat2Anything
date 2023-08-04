from flask import Flask

from .admin import admin_cli


def init_script(app: Flask):
    app.cli.add_command(admin_cli)
