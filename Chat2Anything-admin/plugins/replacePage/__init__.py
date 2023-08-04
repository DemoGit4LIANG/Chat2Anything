"""
初始化插件
"""
import os
from flask import Flask, render_template_string

# 获取插件所在的目录（结尾没有分割符号）
dir_path = os.path.dirname(__file__).replace("\\", "/")
folder_name = dir_path[dir_path.rfind("/") + 1:]  # 插件文件夹名称

def event_init(app: Flask):
    """初始化完成时会调用这里"""
    # 使用下面的代码 查看所有注册的视图函数。对于 Flask app.route 函数的实现，请参考 https://www.jianshu.com/p/dff3bc2f4836
    # print(app.view_functions)
    
    # 定义新视图函数
    def new_index():
        # 规避 render_template 的做法
        with open(dir_path + "/templates/replacePage_index.html", "r", encoding='utf-8') as f:
            return render_template_string(f.read())
    
    # Index.index 是主页的视图函数对应的名称，原视图函数位于 applications/view/index/index.py
    del app.view_functions['Index.index']  # 释放原视图函数
    app.view_functions['Index.index'] = new_index  # 替换原视图函数
    
    