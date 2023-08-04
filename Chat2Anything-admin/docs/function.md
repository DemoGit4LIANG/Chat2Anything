## 用户权限判断

Pear Admin Flask 项目中集成很多实用的功能，为了便于二次开发，同样也提供了许多便于开发的自定义函数。

Pear Admin Flask 项目支持多用户，不同用户有不同的权限，此处将介绍 Pear Admin Flask 中的权限管理函数的用法。

### 函数原型

函数调用位于项目代码 ```applications/common/utils/rights.py``` 中，函数原型如下：

```python
def authorize(power: str, log: bool = False):
    """
    用户权限判断，用于判断目前会话用户是否拥有访问权限

    :param power: 权限标识
    :type power: str
    :param log: 是否记录日志, defaults to False
    :type log: bool, optional
    """
    ...
```

### 基本用法

+ 后端用法

```python
from applications.common.utils.rights import authorize

@app.route("/test")
@authorize("system:power:remove", log=True)
def test_index():
    return 'You are allowed.'
```

> 使用装饰器 @authorize时需要注意，该装饰器需要写在	@app.route之后

+ 前端用法

在前端中，例如增加，删除按钮，对于没有编辑权限的用户不显示的话，可以使用

 `{% **if** authorize("admin:user:edit") %}`

 `{% endif %}`

例如

```python
	{% if authorize("system:user:edit") %}
        <button class="pear-btn pear-btn-primary pear-btn-sm" lay-event="edit">
    	<i class="pear-icon pear-icon-edit"></i>
        </button>
    {% endif %}
    {% if authorize("system:user:remove") %}
        <button class="pear-btn pear-btn-danger pear-btn-sm" lay-event="remove">
        <i class="pear-icon pear-icon-ashbin"></i>
        </button>
    {% endif %}
```

## Schema 序列化

项目中时常会涉及到数据库的读写，在读入数据时可以采用SQLalchemy，将模型查询的数据对象转化为字典。

> Schema 是序列化类，我们把他放在了models文件里，因为觉得没有必要新建一个文件夹叫 Schema ，也方便看着模型写序列化类。

```python
# 例如
class DeptSchema(ma.Schema):  # 序列化类
    deptId = fields.Integer(attribute="id")
    parentId = fields.Integer(attribute="parent_id")
    deptName = fields.Str(attribute="dept_name")
    leader = fields.Str()
    phone = fields.Str()
    email = fields.Str()
    address = fields.Str()
    status = fields.Str()
    sort = fields.Str()
```

> 这一部分有问题的话请看 marshmallow 文档

### 模型到字典

#### 函数原型

函数调用位于项目代码 ```applications/common/curd.py``` 中，函数原型如下：

```
def model_to_dicts(schema: ma.Schema, data):
    """
    将模型查询的数据对象转化为字典
    
    :param schema: schema类
    :param model: sqlalchemy查询结果
    :return: 返回单个查询结果
    """
    ...
```

#### 基本用法

+ model写的是查询后的对象

```python
from applications.common import curd
from applications.models import Dept
from applications.schemas import DeptOutSchema

def test():  # 某函数内
    dept = Dept.query.order_by(Dept.sort).all()
    res = curd.model_to_dicts(Schema=DeptOutSchema, model=dept)
```

## 查询多字段构造器

```python
# 准确查询字段
# 不等于查询字段
# 大于查询字段
# 小于查询字段
# 模糊查询字段(%+xxx+%)
# 左模糊 (% + xxx) 
# 右模糊查询字段(xxx+ %)
# 包含查询字段
# 范围查询字段
# 查询
```

## xss过滤

### 函数原型

函数调用位于项目代码 ```applications/common/utils/validate.py``` 中，函数原型如下：

```
def str_escape(s: str) -> str:
    """
    xss过滤，内部采用flask自带的过滤函数。
    与原过滤函数不同的是此过滤函数将在 s 为 None 时返回 None。

    :param s: 要过滤的字符串
    :type s: str
    :return: s 为 None 时返回 None，否则过滤字符串后返回。
    :rtype: str
    """
    ...
```

### 使用方法

```python
from applications.common.utils.validate import str_escape
real_name = xss_escape(request.args.get('realName', type=str))
```


## 邮件发送

+ 原邮件发送函数

### 函数原型

函数调用位于项目代码 ```applications/common/utils/mail.py``` 中，函数原型如下：

```
def send_mail(subject, recipients, content):
    """原发送邮件函数，不会记录邮件发送记录

    失败报错，请注意使用 try 拦截。

    :param subject: 主题
    :param recipients: 接收者 多个用英文分号隔开
    :param content: 邮件 html
    """
    ...
```

### 示例代码

```python
#在.flaskenv中配置邮箱
from applications.common.utils import mail

mail.send_mail（"subject", "test@test.com", "<h1>Hello</h1>")
```

+ 基于二次开发的邮件发送函数

### 函数原型

函数调用位于项目代码 ```applications/common/utils/mail.py``` 中，函数原型如下：

```
def add(receiver, subject, content, user_id):
    """
    发送一封邮件，若发送成功立刻提交数据库。

    :param receiver: 接收者 多个用英文逗号隔开
    :param subject: 邮件主题
    :param content: 邮件 html
    :param user_id: 发送用户ID（谁发送的？） 可以用 from flask_login import current_user ; current_user.id 来表示当前登录用户
    :return: 成功与否
    """
    ...
```

### 示例代码

```python
#在.flaskenv中配置邮箱
from applications.common.utils import mail

mail.add("test@test.com", "subject", "<h1>Hello</h1>", current_user)
```



## 返回格式

> 后端响应时我们推荐使用规定的API响应格式。

### 函数原型

函数调用位于项目代码 ```applications/common/utils/http.py``` 中，函数原型如下：

```
def success_api(msg: str = "成功"):
    """ 成功响应 默认值“成功” """
    return jsonify(success=True, msg=msg)


def fail_api(msg: str = "失败"):
    """ 失败响应 默认值“失败” """
    return jsonify(success=False, msg=msg)


def table_api(msg: str = "", count=0, data=None, limit=10):
    """ 动态表格渲染响应 """
        res = {
            'msg': msg,
            'code': 0,
            'data': data,
            'count': count,
            'limit': limit

        }
        return jsonify(res)
```

### 示例代码

```python
from applications.common.utils.http import success_api, fail_api, table_api

@admin_log.get('/operateLog')
@authorize("system:log:main")
def operate_log():
    # orm查询
    # 使用分页获取data需要.items
    log = AdminLog.query.filter(
        AdminLog.url != '/passport/login').order_by(
        desc(AdminLog.create_time)).layui_paginate()
    count = log.total
    return table_api(data=model_to_dicts(schema=LogOutSchema, data=log.items), count=count)
```

```python
from applications.common.utils.http import success_api, fail_api, table_api

@admin_power.post('/save')
@authorize("system:power:add", log=True)
def save():
    ...  # 若干操作
    if success:
        return success_api(msg="成功")
    return fail_api(msg="成功")    
```
