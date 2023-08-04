"""
集成了对 Pear Admin Flask 二次开发的的邮件操作，并给了相对应的示例。
"""
from flask import current_app
from flask_mail import Message

from applications.common.curd import model_to_dicts
from applications.common.helper import ModelFilter
from applications.extensions import db, flask_mail
from applications.extensions.init_mail import mail
from applications.models import Mail
from applications.schemas import MailOutSchema


def get_all(receiver=None, subject=None, content=None):
    """
    获取邮件

    返回的列表中的字典构造如下::

        {
            "content": "",  # html内容
            "create_at": "2022-12-25T10:51:17",  # 时间
            "id": 17,  # 邮件ID
            "realname": "超级管理",  # 创建者
            "receiver": "",  # 接收者
            "subject": ""  # 主题
        }

    :param receiver: 发送者
    :param subject: 邮件标题
    :param content: 邮件内容
    :return: 列表
    """
    # 查询参数构造
    mf = ModelFilter()
    if receiver:
        mf.contains(field_name="receiver", value=receiver)
    if subject:
        mf.contains(field_name="subject", value=subject)
    if content:
        mf.exact(field_name="content", value=content)
    # orm查询
    # 使用分页获取data需要.items
    mail = Mail.query.filter(mf.get_filter(Mail)).layui_paginate()
    return model_to_dicts(schema=MailOutSchema, data=mail.items)


def add(receiver, subject, content, user_id):
    """
    发送一封邮件，若发送成功立刻提交数据库。

    :param receiver: 接收者 多个用英文分号隔开
    :param subject: 邮件主题
    :param content: 邮件 html
    :param user_id: 发送用户ID（谁发送的？） 可以用 from flask_login import current_user ; current_user.id 来表示当前登录用户
    :return: 成功与否
    """
    try:
        msg = Message(subject=subject, recipients=receiver.split(";"), html=content)
        flask_mail.send(msg)
    except BaseException as e:
        current_app.log_exception(e)
        return False

    mail = Mail(receiver=receiver, subject=subject, content=content, user_id=user_id)

    db.session.add(mail)
    db.session.commit()
    return True


def delete(id):
    """
    删除邮件记录，立刻写入数据库。

    :param id: 邮件ID
    :return: 成功与否
    """
    res = Mail.query.filter_by(id=id).delete()
    if not res:
        return False
    db.session.commit()
    return True

def send_mail(subject, recipients, content):
    """原发送邮件函数，不会记录邮件发送记录

    失败报错，请注意使用 try 拦截。

    :param subject: 主题
    :param recipients: 接收者 多个用英文分号隔开
    :param content: 邮件 html
    """
    message = Message(subject=subject, recipients=recipients, html=content)
    mail.send(message)
