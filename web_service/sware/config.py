#!/usr/bin python
# -*-coding:utf-8-*-
# author:sware
# 定义一些工程常用的配置


import os

# 获取当前目录路径
basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    # 配置秘钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'this is a secret string'
    SQLALCHEMY_TRACK_MODIFICATIONS = True

    # 配置上传文件存储地址
    UPLOADED_PHOTOS_DEST = os.getcwd()+'/tmpfile'

    """
    Flask-Mail 服务器配置
    MAIL_SERVER = 'smtp.qq.com'
    MAIL_PORT = 465
    
    MAIL_SERVER = 'smtp.126.com'
    MAIL_PORT = 25
    
    MAIL_SERVER = 'smtp.163.com'
    MAIL_PORT = 465
    

    其中用户名和密码可以配置在环境变量中：
    export MAIL_USERNAME=<Gmail username>
    export MAIL_PASSWORD=<Gmail password>
    
    环境变量中获取用户名和密码
    os.environ.get('MAIL_USERNAME')
    os.environ.get('MAIL_PASSWORD')
    """

    # 126邮箱配置
    # 电子邮件服务器的主机名或IP地址
    MAIL_SERVER = 'smtp.126.com'
    # 电子邮件服务器的端口 25 465[加密使用 目前来看邮件发送本身没有问题，但是在阿里云上一直发送不了，问题出现在连接126服务器上]
    # 阿里云服务器 ECS 基于安全考虑，目前已禁用 25 端口。
    MAIL_PORT = 25
    # 启用传输层安全(Transport Layer Security, TLS)协议
    MAIL_USE_TLS = True
    # 启用安全套接层(Secure Sockets Layer, SSL)协议
    MAIL_USE_SSL = False
    # 邮件账户的用户名
    MAIL_USERNAME = 'sunlxt123@126.com'
    # 邮件账户的密码
    MAIL_PASSWORD = 'zxcvbnm789'
    # 邮件发件人
    MAIL_DEFAULT_SENDER = 'sunlxt123@126.com'


    # 邮件批量发送个数上线
    MAIL_MAX_EMAILS = None
    # 是否为debug状态
    MAIL_DEBUG = True
    # 可以理解为邮件主题
    FLASKY_MAIL_SUBJECT_PREFIX = '[Sware Blog]'
    # 发件人
    FLASKY_MAIL_SENDER = 'Sware Admin <sunlxt123@126.com>'
    # 定义管理员邮箱，通过邮箱判断管理员角色 定义为列表方便生成多位管理员
    FLASKY_ADMIN = ['sunlxt123@126.com',]



    # 装饰器，使类的方法可以当函数使用
    @staticmethod
    def init_app(app):
        pass


class DevelopmentConfig(Config):
    """
    默认配置
    """
    # mysql database config
    # 数据库的基础配置信息
    USERNAME = 'admin'
    PASSWORD = '1234'
    HOST = '47.94.88.67'
    PORT = '3306'
    DATABASE = 'swares'

    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI



class TestingConfig(Config):
    '''
    测试配置信息，邮件和数据
    '''
    # mysql database config
    # 数据库的基础配置信息
    USERNAME = 'admin'
    PASSWORD = '1234'
    HOST = 'localhost'
    PORT = '3306'
    DATABASE = 'swares'

    DB_URI = 'mysql+pymysql://{}:{}@{}:{}/{}?charset=utf8'.format(USERNAME, PASSWORD, HOST, PORT, DATABASE)
    SQLALCHEMY_DATABASE_URI = DB_URI



config = {
    'testing': TestingConfig,

    # default setting
    'default': DevelopmentConfig
}


if __name__ == "__main__":
    a = Config()
    print(config['testing'].config)


