from applications.view.system import register_system_bps
from applications.view.plugin import register_plugin_views
from applications.view.knowledge import register_knowledge_bps


def init_bps(app):
    register_system_bps(app)
    register_plugin_views(app)
    register_knowledge_bps(app)
