# -*- coding:utf-8 -*-
# author:sware
# date:2018-01-18
# 邮件发送模块

import os
from . import mail
from flask_mail import Message
# 导入current_app 代替 app
from flask import current_app,render_template
from threading import Thread

# 引入日志模块
import logging

logger = logging.getLogger('example02.email')
# logger.info('logger of mod say something...')


def send_async_email(app,msg):
    """
    app_context() 手动创建应用上下文
    """
    with app.app_context():
        # 在线程中发送邮件，避免页面挂死
        logging.debug(u'在send_async_email 中的 发件人：{} 收件人：{}'.format(msg.sender, msg.recipients))
        maslog = mail.send(msg)
        logging.debug(u'mail.send success : {} maslog: {}'.format(msg.subject, maslog))



def send_email(to,subject,template,**kwargs):
    """
    current_app是一个本地代理，它的类型是werkzeug.local. LocalProxy，它所代理的即是我们的app对象
    current_app == LocalProxy(app)。
    使用current_app是因为它也是一个ThreadLocal变量，对它的改动不会影响到其他线程。
    可以通过current_app._get_current_object()方法来获取app对象

    :param to: 表示发送给谁
    :param subject: 主题
    :param template: 模板
    :param kwargs: 其他参数
    :return: None
    """
    # 获取app 对象， current_app 只能在请求线程里存在，因此它的生命周期也就在应用上下文里
    app = current_app._get_current_object()

    # 创建一个消息实例发送消息，配置主题，设置发件人，收件人
    # 当配置 FLASK_MAIL_SENDER 后不需要在配置 sender 默认使用 FLASK_MAIL_SENDER 配置值
    # 163在给别人发的同时给自己也发一封邮件就不会报错
    msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,sender=current_app.config['MAIL_DEFAULT_SENDER']
                  ,recipients=[to,current_app.config['MAIL_DEFAULT_SENDER']])
    logging.debug(u'msg.subject: {} msg.recipients: {} '.format(msg.subject,msg.recipients))
    logging.debug(u'发件人：{} 收件人：{}'.format(msg.sender ,msg.recipients))

    # 配置消息体
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    logging.debug(u'msg.subject: {} msg.recipients: {} '.format(msg.body,msg.html))

    # 创建新线程
    thr = Thread(target=send_async_email, args=[app,msg])
    # 启动线程
    thr.start()

    # 返回线程
    return thr






#
# def send_email(to,subject,template,**kwargs):
#     """
#     :param to: 表示发送给谁
#     :param subject: 主题
#     :param template: 模板
#     :param kwargs: 其他参数
#     :return: None
#     """
#     # 创建一个消息实例发送消息，配置主题，设置发件人，收件人
#     # 当配置 FLASK_MAIL_SENDER 后不需要在配置 sender 默认使用 FLASK_MAIL_SENDER 配置值
#     msg = Message(current_app.config['FLASKY_MAIL_SUBJECT_PREFIX'] + subject,recipients=[to])
#     logging.debug('msg.subject: %s msg.recipients: %s '.format(msg.subject,msg.recipients))
#
#     # 配置消息体
#     msg.body = render_template(template + '.txt', **kwargs)
#     msg.html = render_template(template + '.html', **kwargs)
#     logging.debug('msg.subject: %s msg.recipients: %s '.format(msg.body,msg.html))
#
#     # 发送信息，在发送的时候页面会挂死
#     mail.send(msg)
#     logging.debug('mail.send success %s '.format(msg.subject))





