#!/usr/bin python
#-*-coding:utf-8-*-
#
"""
表单类
"""

from wtforms import StringField,SubmitField,PasswordField,BooleanField
from wtforms.validators import  DataRequired,Length,Email,Regexp,EqualTo
from wtforms import ValidationError
from flask_wtf import FlaskForm
from ..models.model import User


# 文件上传表单
from flask_wtf.file import FileField,FileRequired,FileAllowed
from .. import photos



#用户登录表单
class LoginForm(FlaskForm):
    # 用户的文本字段
    username=StringField('what is your name',validators=[DataRequired()])
    # 密码字段 PasswordField 类表示属性为 type="password" 的 <input> 元素
    password=PasswordField('what is your password',validators=[DataRequired()])
    # 记住我的复选框 BooleanField 类表示复选框
    remember_me = BooleanField('Keep me logged in')
    # 提交按钮
    submit=SubmitField('Login in')


#用户注册表单
class RegisterForm(FlaskForm):
    # 电子邮件地址文本字段 Length() Email() 验证函数
    email=StringField('your Email addersss',validators=[DataRequired(),Length(1,64),Email()])
    # 用户名文本字段
    username=StringField('your name',validators=[DataRequired(),Length(1,64),
        Regexp('^[A-Za-z0-9_.]*$',0,'用户名只能是数字与字母下划线以及点')])
    # 密码字段
    password=PasswordField('your password',validators=[DataRequired(),Length(1,64),
        EqualTo('password2', message='Passwords must match.')])
    # 密码二次验证
    password2 = PasswordField('Confirm password',validators=[DataRequired(),Length(1,64)])
    # 提交按钮
    submit=SubmitField('register')

    """
    表单还有两个自定义的验证函数，以方法的形式实现。如果表单类中定义了以
    validate_ 开头且后面跟着字段名的方法，这个方法就和常规的验证函数一起调用
    """
    def validate_email(self,field):
        # 判断邮箱是否已经注册，如果已经注册抛出异常
        if User.query.filter_by(email = field.data).first():
            raise ValidationError('Email already registered.')

    def validate_username(self,field):
        if User.query.filter_by(username = field.data).first():
            raise  ValidationError('User name already in use.')


#用户文章发表更新表单
class PostForm(FlaskForm):
    title=StringField('This is title',validators=[DataRequired()])
    text=StringField('分享一下你的心情',validators=[DataRequired()])
    submit=SubmitField('post')


# 图片上传表单
class UploadForm(FlaskForm):
    photo = FileField(
        validators=[
            FileAllowed(photos,u'只能上传图片！'),
            FileRequired(u'文件未选择！')
        ]
    )
    submit = SubmitField(u'上传')