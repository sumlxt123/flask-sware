#!/usr/bin python
# -*-coding:utf-8-*-
# 视图

from flask import render_template,abort,flash,redirect,url_for,request
from . import main
from .. import db
from ..models.model import Permission,User,Role

from flask_login import login_required
from ..decorators import admin_required,permission_required



# 引入日志模块
import logging

# logger = logging.getLogger('sware.main')
logger = logging.getLogger('example02.main')
# logger.info('logger of mod say something...')


@main.route("/")
def index():
    logger.info('logger of the is index views!!!...')
    return render_template('index.html')

@main.route("/user/<username>")
def user(username):
    """用户的资料路由"""
    user = User.query.filter_by(username=username).first()
    logging.debug("main user on username: ".format(user))

    if user is None:
        abort(404)

    return render_template('main/user.html',user=user)



@main.route("/admin")
@login_required
@admin_required
def for_admins_only():
    logger.info('the is main admin route.')
    return render_template('main/admin.html')


@main.route("/moderator")
@login_required
@permission_required( Permission.MODERATE_COMMENTS)
def for_moderators_only():
    return render_template('main/moderator.html')

