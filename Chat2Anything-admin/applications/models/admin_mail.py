import datetime
from applications.extensions import db


class Mail(db.Model):
    __tablename__ = 'admin_mail'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='邮件编号')
    receiver = db.Column(db.String(1024), comment='收件人邮箱')
    subject = db.Column(db.String(128), comment='邮件主题')
    content = db.Column(db.Text(), comment='邮件正文')
    user_id = db.Column(db.Integer, comment='发送人id')
    create_at = db.Column(db.DateTime, default=datetime.datetime.now, comment='创建时间')
