#!/usr/bin python
# -*-coding:utf-8-*-
# 视图
from . import auth
from .. import db,photos
from ..email import send_email
from ..models.model import User,Role
from ..forms.form import LoginForm,RegisterForm,UploadForm
from flask import render_template,flash,redirect,url_for,request

from flask_login import login_user,logout_user,login_required,\
    current_user



# 引入日志模块
import logging

# logger = logging.getLogger('sware.auth')
logger = logging.getLogger('example02.auth')
# logger.info('logger of mod say something...')


@auth.before_app_request
def before_request():
    """
    对于蓝本来说， before_request 钩子只能应用属于蓝本的请求上。
    如果想在蓝本中使用正对于程序全局请求的钩子，必须使用before_app_request修饰器

    处理程序中过滤未确认的账户

    当满足以下条件时，before_app_request 处理程序会拦截请求，会被重定向到 /auth/unconfirmed 路由
    用户已登录 current_user.is_authenticated
    用户账户还未确认
    请求的端点不在认证蓝本中 request.endpint
    :return:
    """
    if current_user.is_authenticated:
        # 更新用户最后一次登录时间
        current_user.ping()
        if not current_user.confirmed \
            and request.endpoint \
            and request.blueprint != 'auth' \
            and request.endpoint != 'static':
            # current_user 只在上下文中有效
            # logging.debug("current_user.confirmed：{} ".format(current_user.cofirmed))
            logging.debug(u"auth before_request in request.blueprint: {}".format(request.blueprint))
            return  redirect( url_for('auth.unconfirmed') )


@auth.route('/unconfirmed')
def unconfirmed():
    """
    未验证用户提醒确认路由
    """
    if current_user.is_anonymous() or current_user.confirmed:
        logging.debug(u"auth views unconfirmed in current_user.is_anonymous: {} current_user.confirmed: {}".format(current_user.is_anonymous(),current_user.confirmed))
        return redirect( url_for('main.index') )

    return render_template('auth/unconfirmed.html')


@auth.route('/confirm')
@login_required
def resend_confirmation():
    """重新发送账户确认邮件"""
    token = current_user.generate_confirmation_token()
    send_email(current_user.email,'Confirm Your Account','mail/new_user',user = current_user,token = token)
    flash("A new confirmation email has been sent to you by email.")
    return redirect( url_for('main.index') )



@auth.route("/login", methods=['POST', 'GET'])
def login():
    """
    登录路由：当请求是GET 时，视图函数直接渲染模板，及显示表单，当表单在 POST 请求中提交时，
    Flask-WTF 中的 validate_on_submit() 函数会验证表单数据，然后尝试登入用户。

    :return:
    """
    user = None
    # 实例化登录表单
    form = LoginForm()

    # 判断是否验证提交
    if form.validate_on_submit():
        logger.debug('form.username: {} form.password: {}'.format(form.username.data,form.password.data) )
        # 从数据库查询数据
        user = User.query.filter_by(username=form.username.data ).first()
        logger.debug('database data : %s' %user)
        # 用户存在则进一步判断密码是否输入正确
        if user is not None:
            # 当用户存在，且密码正确时返回登录成功页面 否则认为登录失败返回登录页面
            if user is not None and user.verify_password(form.password.data):
                # login_user() 方法会把用户标记为已登录，login_user()函数的参数是要登录的用户，以及可选的 记住我 布尔值
                login_user(user,form.remember_me.data)
                logging.debug("views login in user: {} remember_me: {}".format(user,form.remember_me.data))
                flash('Login success !!!')
                return redirect( url_for('main.index'))
            else:
                flash('user password error !!!')
                return render_template('auth/login.html', form=form)
        else:
            flash('User does not exist, Please register user !!!')
            return redirect( url_for('auth.login') )


    return render_template('auth/login.html', form=form)




@auth.route("/register", methods=['POST', 'GET'])
def register():
    """
    注册路由
    :return:
    """
    user = None
    form = RegisterForm()
    logger.debug('form ： %s'.format(form))

    # 判断是否验证提交
    if  form.validate_on_submit():
        logger.debug('form.username: %s form.password: %s' % (form.username.data,form.password.data) )

        # 在注册前先判断用户是否存在 不存在则注册用户 存在则提示已注册
        user = User.query.filter_by(username=form.username.data).first()
        logger.debug('user name : {}'.format( user) )
        if user is None:
            # 初始化用户类
            user = User(username = form.username.data,password = form.password.data,email = form.email.data)
            logger.debug('user class instance is : {}'.format(user))
            # 向数据库添加数据
            db.session.add(user)
            # 提交数据
            db.session.commit()

            """用户登录成功后，发送邮件进行验证"""
            token = user.generate_confirmation_token()
            logging.info('views in register token: {}'.format(token))
            # 向发送邮件方法传入相关参数
            send_email(user.email,"Confirm Your Account",'mail/new_user',user = user, token = token)

            # 提示信息
            flash('User register success !!!')
            # 在蓝图的视图中使用 url_for() 时需要添加蓝图前缀，否则会报错
            # 注册成功后返回到登录页面
            return redirect( url_for('auth.login'))
        else:
            flash('User does is exist, Please login .')
            return redirect( url_for('auth.register') )


    return render_template('auth/register.html', form = form )


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    """
    确认账户的视图函数
    login_required 修饰器保护路由，
    :param token:
    :return:
    """
    # 先检查已登录用户是否已经确认过，如果确认过，则重定向到首页，防止多次点击确认令牌的情况
    if current_user.confirmed:
        return redirect( url_for('main.index') )

    # 确认令牌已经在 user 模型中完成，所以视图函数只需要调用即可
    # 然后在根据确认结果显示不同Flash消息。
    # 确认成功后， User 模型中 confirmed 属性的值会被修改并添加到会话中，
    # 请求处理完后，这两个操作被提交到数据库
    logging.info("views in current_user.confirm(token): {}".format(current_user.confirm(token)))
    if current_user.confirm(token):
        flash('You have confirmed your account. Thanks!')
    else:
        flash('The confirmation link is invalid or has expired.')
    return redirect(url_for('main.index'))


@auth.route("/logout", methods=['POST', 'GET'])
@login_required
def logout():
    """
    用户登出：退出路由
    调用 flask-login 中的 logout_user() 函数，删除并重新设置用户会话。
    随后显示一个 Flash 消息，确认这次操作，再重定向到首页，完成登出
    """
    logout_user()
    flash("You have been logged out")
    return redirect( url_for('main.index'))






@auth.route('/uploadfile', methods=['POST', 'GET'])
@login_required
def uploadfile():
    """
    实现图片上传：login_required 起路由保护的作用，未登录用户无法上传图片
    实现图片上传
    """
    namee = None
    # 实例化表单
    form = UploadForm()
    if form.validate_on_submit():
        filename = photos.save(form.photo.data)
        # 返回一个文件的url
        file_url = photos.url(filename)
        namee = 'validate_on_submit ！！！！'
    else:
        file_url = None
        namee = 'the is else!!!'

    return render_template('auth/uploadform.html',form=form ,file_url=file_url,nameeee=namee )



