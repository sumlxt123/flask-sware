# -*-coding:utf-8-*-
#
# 用于启动程序以及其他的程序任务


import os
from flask_script import Manager,Shell,Command
from flask_migrate import Migrate,MigrateCommand


# 导入自定义的初始化函过程，与数据库
from sware import create_app,db
from sware.models.model import User,Role
from sware import forms

# default 默认为阿里云的配置
# testing 为本地配置
app = create_app('testing')

manager = Manager(app)

# 创建数据库迁移对象
migrate = Migrate(app,db)


# 以装饰器的方式添加命令行命令用于初始化数据
@manager.command
def insertdb():
    from flask_migrate import upgrade
    upgrade()
    Role.insert_roles()
    # User.insert_users()

# 增加命令行操作的命令两种方式
# def make_shell_context():
#     return dict(app=app,db=db,User=User,Role=Role,)
#
# manager.add_command("shell",Shell(make_context=make_shell_context))

@manager.shell
def make_shell_context():
    return dict(app=app,db=db,User=User,Role=Role)

# 增加命令行操作的命令
manager.add_command('db',MigrateCommand)


if __name__ == "__main__":
    import sys
    # 将标准输出在重定向前进行保存，由于使用后恢复正常
    saveerr = sys.stderr
    # 打开一个新文件用于希尔
    fsock = open('./log/error.log', 'w')
    # 将所有后续输出重定向到我们刚刚打开的新文件上
    sys.stderr = fsock

    # 启动应用
    manager.run()

    # 将标准输出恢复到原来的方式
    # sys.stderr = saveerr
    # 关闭日志文件
    # fsock.close()


