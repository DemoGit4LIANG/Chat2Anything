import shutil

from flask import Flask
from flask import Blueprint, render_template, request, jsonify, escape
from applications.common.utils.http import table_api, fail_api, success_api
import os
import json
import traceback
import importlib

from applications.common.utils.rights import authorize

plugin_bp = Blueprint('plugin', __name__, url_prefix='/plugin')
PLUGIN_ENABLE_FOLDERS = []

def register_plugin_views(app: Flask):
    global PLUGIN_ENABLE_FOLDERS
    app.register_blueprint(plugin_bp)
    # 载入插件过程
    # plugin_folder 配置的是插件的文件夹名
    PLUGIN_ENABLE_FOLDERS = app.config['PLUGIN_ENABLE_FOLDERS']
    for plugin_folder in PLUGIN_ENABLE_FOLDERS:
        plugin_info = {}
        try:
            with open("plugins/" + plugin_folder + "/__init__.json", "r", encoding='utf-8') as f:
                plugin_info = json.loads(f.read())
            # 初始化完成事件
            try:
                getattr(importlib.import_module('plugins.' + plugin_folder), "event_init")(app)
            except AttributeError:  # 没有插件启用事件就不调用
                pass
            except BaseException as error:
                return fail_api(msg="Crash a error! Info: " + str(error))
            print(f" * Plugin: Loaded plugin: {plugin_info['plugin_name']} .")
        except BaseException as e:
            info = f" * Plugin: Crash a error when loading {plugin_info['plugin_name'] if len(plugin_info) != 0 else 'plugin'} :" + "\n"
            info += 'str(Exception):\t' + str(Exception) + "\n"
            info += 'str(e):\t\t' + str(e) + "\n"
            info += 'repr(e):\t' + repr(e) + "\n"
            info += 'traceback.format_exc():\n%s' + traceback.format_exc()
            print(info)
