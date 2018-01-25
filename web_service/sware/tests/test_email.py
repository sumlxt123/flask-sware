# -*-coding:utf-8-*-
# 邮件发送脚本
# author:sware
# date:2018-01-17

from flask import Flask
from flask_mail import Mail,Message
import os



# class config:
#     SECRET_KEY = 'hard to guess string'
#     MAIL_SERVER = 'smtp.126.com'
#     MAIL_PROT = 25
#     MAIL_USE_TLS = False
#     MAIL_USE_SSL = False
#     MAIL_USERNAME = "sunlxt123@126.com"
#     MAIL_PASSWORD = "zxcvbnm789"
#     MAIL_DEBUG = True

app = Flask(__name__)

app.config.update(
    SECRET_KEY='hard to guess string',
    MAIL_SERVER = 'smtp.126.com',
    MAIL_PROT = 994,
    MAIL_USE_TLS = True,
    MAIL_USE_SSL = False,
    MAIL_USERNAME = "sunlxt123@126.com",
    MAIL_PASSWORD = "zxcvbnm789",
    MAIL_DEBUG = True,
)

mail = Mail(app)


@app.route('/')
def index():
    # sender 发送方，recipients 邮件接收方列表
    msg = Message('Hi!This is a test',sender='sunlxt123@126.com',recipients=['lixingt@outlook.com','sunlxt123@126.com'])
    # msg.body 邮件正文
    msg.body = "This is a there Ecs on first email."
    # msg.attach 邮件附件添加啊
    # msg.attach("文件名","类型",读取文件)
    with app.open_resource("./my.jpg") as fp:
        msg.attach("my.jpg","image/jpg",fp.read())

    mail.send(msg)
    print("mail sent")
    return '<h1>Sent</h1>'

if __name__ == "__main__":
    app.run(host='0.0.0.0',port=8080)





