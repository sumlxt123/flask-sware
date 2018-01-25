#!/usr/bin python
# -*-coding:utf-8-*-
# __all__ = ['models','forms','static','templates','main']

from flask import Flask
from flask_bootstrap import Bootstrap

# sqlalchemy模块引用
from flask_sqlalchemy import SQLAlchemy

# 引用flask_uploads 用于配置上传信息
from flask_uploads import UploadSet, configure_uploads, IMAGES, patch_request_class

# 引用登录扩展
from flask_login import LoginManager

# 引用邮件发送模块
from flask_mail import Mail

# 引用 JavaScript 日期处理库
from flask_moment import Moment



# 引用日志模块
import logging
import logging.config

# config 在当前目录之上，可能会存在引用问题
from config import config


# 实例化
bootstrap = Bootstrap()
db = SQLAlchemy()

# 实例化set类 ， 只允许上传图片
photos = UploadSet('photos', IMAGES)


# 初始化 Flask_Login
login_manager = LoginManager()
# session_protection 属性可以设为 None 、 'basic' 或 'strong' ，
# 以提供不同的安全等级防止用户会话遭篡改。设为 'strong' 时，
# Flask-Login 会记录客户端 IP 地址和浏览器的用户代理信息，如果发现异动就登出用户
login_manager.session_protection = "strong"
# 涉及登录页面的路由
login_manager.login_view = 'auth.login'

# 实例化邮件实体
mail = Mail()

# 实例化日期处理类
moment = Moment()

# 实例化日志记录器,引入日志配置文件 通过实例化记录器的名称达到控制日志级别的目的
logging.config.fileConfig("logging.conf")
# 共创建三个Logger：
# root，将所有日志输出至控制台，将所有日志写入文件；
# example01，将所有日志输出至控制台，将所有日志写入文件；
# example02，将级别大于或等于INFO的日志输出至控制台，将级别大于或等于WARNING的日志写入文件
logger = logging.getLogger('example02')

#用于测试日志配置
# logger.debug('This is debug message')
# logger.info('This is info message')
# logger.warning('This is warning message')





# 应用初始化
def create_app(config_name):
    # 实例化应用
    app = Flask(__name__)

    # 引用配置信息
    app.config.from_object(config[config_name])
    # 将配置传入应用[此语句貌似有些多余
    config[config_name].init_app(app)

    # 初始化login_manger
    login_manager.init_app(app)

    # 初始化mail
    mail.init_app(app)

    moment.init_app(app)
    
    # 初始化 bootstrap 模板
    bootstrap.init_app(app)

    # 数据库链接初始化
    db.init_app(app)

    # 注册蓝本
    from .main import main as main_blueprint
    app.register_blueprint(main_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    # url_prefix 参数使用后，注册后蓝本中定义的所有路由都会加上指定前缀
    # app.register_blueprint(auth_blueprint,url_prefix='/auth')

    # 注册并完成相应配置配置上传信息
    configure_uploads(app,photos)
    # 上传文件大小限制
    patch_request_class(app)


    # 返回初始化后的应用
    return app










