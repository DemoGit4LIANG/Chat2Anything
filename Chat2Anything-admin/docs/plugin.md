### 说明

插件功能旨在最大限度不修改原框架的前提下添加新功能，我们提供了三个示例插件。


### 插件配置

将插件文件夹放置在 ```applications/config.py``` 文件夹中，并且在 .flaskenv 中配置。再配置项中填入插件的文件夹名，已 json 格式写入其中。

```python
# 插件配置
PLUGIN_ENABLE_FOLDERS = ["helloworld"]
```

### 插件目录

```
Plugin
│  __init__.json
└─ __init__.py
```

这是一个非常简单的插件。

### 插件信息

插件信息保存在 ```__init__.py``` 中，以测试插件“helloword”为例。插件的数据应该不少于下面三项：

```json
{
  "plugin_name": "Hello World",
  "plugin_version": "1.0.0.1",
  "plugin_description": "一个测试的插件。"
}
```

### 插件格式

插件的入口点为 ```__init__.py``` 文件，在插件被启用后，程序启动时此 Python 文件中的 ```event_init``` 函数。代码如下：

```python
from flask import Flask

def event_init(app: Flask):
    """初始化完成时会调用这里"""
    print("加载完毕后，我会输出一句话。")
```