from applications.extensions import ma
from marshmallow import fields
from applications.models import User


# 用户models的序列化类
class MailOutSchema(ma.Schema):
    id = fields.Integer()
    receiver = fields.Str()
    subject = fields.Str()
    content = fields.Str()
    realname = fields.Method("get_realname")
    create_at = fields.DateTime()

    def get_realname(self, obj):
        if obj.user_id != None:
            return User.query.filter_by(id=obj.user_id).first().realname
        else:
            return None
