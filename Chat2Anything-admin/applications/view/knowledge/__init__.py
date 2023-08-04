
from flask import Flask, Blueprint
from applications.view.knowledge.knowledge_store import bp as store_bp

knowledge_bp = Blueprint('knowledge', __name__, url_prefix='/knowledge')


def register_knowledge_bps(app: Flask):
    knowledge_bp.register_blueprint(store_bp)
    app.register_blueprint(knowledge_bp)