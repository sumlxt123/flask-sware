# -*- coding:utf-8 -*-
# 自定义装饰器




from functools import wraps
from flask import abort
from flask_login import current_user
from .models.model import Permission





def permission_required(permission):
    """定义检查用户权限的自定义修饰器"""
    def decorator(f):
        # wraps 装饰器避免自定义装饰器对于程序的影响（函数名等函数属性等会发生改变)
        @wraps(f)
        def decorated_function(*args,**kwargs):
            # 如果用户不具有指定权限 则返回 403 错误码
            if not current_user.can(permission):
                abort(403)
            return f(*args,**kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    return permission_required(Permission.ADMINISTER)(f)


