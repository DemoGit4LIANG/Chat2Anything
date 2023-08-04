from applications.extensions import ma
from marshmallow import fields


class KnowledgeStoreOutSchema(ma.Schema):
    id = fields.Integer()
    name = fields.Str()
    create_user_id = fields.Integer()
    create_dept_id = fields.Integer()
    size = fields.Float()
    create_time = fields.DateTime()
    update_time = fields.DateTime()
    desc = fields.Str()
    path = fields.Str()

