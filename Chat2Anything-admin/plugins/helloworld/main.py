from flask import render_template, Blueprint

# 创建蓝图
helloworld_blueprint = Blueprint('hello_world', __name__, template_folder='templates', static_folder="static",
                       url_prefix="/hello_world")

@helloworld_blueprint.route("/")
def index():
    return render_template("helloworld_index.html")

