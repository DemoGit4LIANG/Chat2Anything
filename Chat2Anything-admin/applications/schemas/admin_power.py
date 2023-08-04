from flask_marshmallow.sqla import SQLAlchemyAutoSchema

from applications.extensions import ma
from marshmallow import fields

from applications.models import Power


class PowerSchema(SQLAlchemyAutoSchema):
    class Meta:
        model = Power  # table = models.Album.__table__
        # include_relationships = True  # 输出模型对象时同时对外键，是否也一并进行处理
        include_fk = True  # 序列化阶段是否也一并返回主键
        # fields= ["id","name"] # 启动的字段列表
        # exclude = ["id","name"] # 排除字段列表

# 权限models序列化类
class PowerOutSchema(ma.Schema):
    id = fields.Integer()
    title = fields.Str(attribute="name")
    type = fields.Str()
    code = fields.Str()
    href = fields.Str(attribute="url")
    openType = fields.Str(attribute="open_type")
    parent_id = fields.Integer()
    icon = fields.Str()
    sort = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    enable = fields.Integer()


class PowerOutSchema2(ma.Schema):  # 序列化类
    powerId = fields.Str(attribute="id")
    powerName = fields.Str(attribute="name")
    powerType = fields.Str(attribute="type")
    powerUrl = fields.Str(attribute="url")
    openType = fields.Str(attribute="open_type")
    parentId = fields.Str(attribute="parent_id")
    icon = fields.Str()
    sort = fields.Integer()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    enable = fields.Integer()
