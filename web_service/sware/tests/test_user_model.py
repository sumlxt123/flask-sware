# -*- coding:utf-8 -*-
# author:sware
# 2018-01-16

import unittest
from ..sware.models.model import User, Role, AnonymousUser, Permission


class UserModelTestCase(unittest,TestCase):
    def test_password_setter(self):
        """判断用户密码设置是否为空"""
        u = User(password = 'cat')
        self.asserTrue(u.password_hash is not None)

    def test_no_password_getter(self):
        u = User(password = 'cat')
        with self.asserRaises(AttributeError):
            u.password

    def test_password_verification(self):
        u = User(password = 'cat')
        self.asserTrue(u.verify_password('cat'))
        self.asserFalse(u.verify_password('dog'))

    def test_password_salts_are_random(self):
        u = User(password = 'cat')
        u2 = User(password = 'cat')
        self.assertTrue(u.password_hash != u2.password_hash )

    def test_roles_and_permissions(self):
        """角色单元测试"""
        Role.insert_roles()
        u = User(email='sunlxt123@163.com',password='1234')
        self.assertTrue(u.can(Permission.WRITE_ARTICLES))
        self.assertFalse(u.can(Permission.MODERATE_COMMENTS))


    def test_anonymous_user(self):
        """权限单元测试"""
        u = AnonymousUser()
        self.assertFalse(u.can(Permission.FOLLOW))