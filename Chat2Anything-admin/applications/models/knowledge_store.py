import datetime
from applications.extensions import db


class KnowledgeStore(db.Model):
    __tablename__ = 'knowledge_store'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='知识库ID')
    name = db.Column(db.String(255), nullable=False)
    create_user_id = db.Column(db.Integer)
    create_dept_id = db.Column(db.Integer)
    size = db.Column(db.Float(3), nullable=False)
    create_time = db.Column(db.DateTime)
    update_time = db.Column(db.DateTime)
    desc = db.Column(db.String(255), nullable=True)
    path = db.Column(db.String(255), nullable=False)