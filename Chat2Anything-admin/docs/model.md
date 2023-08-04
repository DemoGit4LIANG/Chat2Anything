## 模型/数据库和序列化
### 数据库连接

项目采用flask-sqlalchemy，支持多数据库连接，默认sqlite

HOSTNAME: 指数据库的IP地址
USERNAME：指数据库登录的用户名
PASSWORD：指数据库登录密码
PORT：指数据库开放的端口
DATABASE：指需要连接的数据库名称
#### mssql
```
MSSQL:    f"mssql+pymssql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=cp936"
```
#### msyql
```
$ pip install pymysql

# 手动在mysql中创建数据库，并将配置文件中的url配置如下示例

SQLALCHEMY_DATABASE_URI =  f"mysql+pymysql://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}?charset=utf8mb4"
```
#### Oracle
```
Oracle:   f"oracle+cx_oracle://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
```
#### SQLite
```
SQLite    "sqlite:/// database.db"
```
#### Postgres
```
Postgres f"postgresql+psycopg2://{USERNAME}:{PASSWORD}@{HOSTNAME}:{PORT}/{DATABASE}"
```


### 序列化

推荐使用这种自动类型的
```python
from flask_marshmallow.sqla import SQLAlchemyAutoSchema
from applications.models import 你的模型类
class RoleOutSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = 你的模型类  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表
```
