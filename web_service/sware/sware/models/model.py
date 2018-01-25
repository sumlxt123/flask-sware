# -*-coding:utf-8-*-
#

from .. import db
from datetime import datetime
from flask import current_app
# 用于实现密码散列
from werkzeug.security import generate_password_hash,check_password_hash

# 引入生成令牌的方法
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

# 引入用户登录
from .. import login_manager
# 引入 UserMixin 用户类，使用时 必须实现 is_authenticated() is_active() is_anonymous() get_id() 方法
# from flask_login import UserMixin
from flask_login import AnonymousUserMixin



# 引入日志模块
import logging

# logger = logging.getLogger('sware.main')
logger = logging.getLogger('example02.model')
# logger.info('logger of mod say something...')



"""
role 与 user 为一对多的关系
"""

class Permission:
    """
    程序的权限定义：Permission 权限常量

    """
    FOLLOW = 0x01 #关注用户
    COMMENT = 0x02 #在他人撰写的文章中发布评论
    WRITE_ARTICLES = 0x04 #写原创文章
    MODERATE_COMMENTS = 0x08 #查处他人发表的不当评论
    ADMINISTER = 0x80 #管理网站


class Role(db.Model):
    # db中的表名，如不设置，可能会与class相同的名称
    __tablename__ = "roles"
    # colums
    # SQLAlchemy要求必须有主键，一般命名为ID即可
    id = db.Column(db.Integer, primary_key=True)
    # 角色名称
    name = db.Column(db.String(64), unique=True)
    # 默认角色标识字段，用户注册时，其角色被设为默认角色
    default = db.Column(db.Boolean, default=False, index=True)
    # 角色权限
    permissions = db.Column(db.Integer)

    """
    backref：用于指定表之间的双向关系，如果在一对多的关系中建立双向的关系，这样的话在对方看来这就是一个多对一的关系
    lazy：指定 SQLAlchemy 加载关联对象的方式。
    lazy=subquery: 会在加载 Post 对象后，将与 Post 相关联的对象全部加载，这样就可以减少 Query 的动作，
    也就是减少了对 DB 的 I/O 操作。但可能会返回大量不被使用的数据，会影响效率。
    
    lazy=dynamic: 只有被使用时，对象才会被加载，并且返回式会进行过滤，
    如果现在或将来需要返回的数据量很大，建议使用这种方式。Post 就属于这种对象。
    """
    users = db.relationship('User', backref='role', lazy='dynamic')



    @staticmethod
    def insert_roles():
        """初始化数据，先查询 判断是否存在，再插入"""
        roles = {
            # 实际上是通过与的方式获得最终的权限值
            # 用户具有发布文章、发表评论和关注其他用户的权限。这是新用户的默认角色
            'User': (Permission.FOLLOW |
                     Permission.COMMENT |
                     Permission.WRITE_ARTICLES, True),
            # 协管员 正价审查不当评论的权限
            'Moderator': (Permission.FOLLOW |
                          Permission.COMMENT |
                          Permission.WRITE_ARTICLES |
                          Permission.MODERATE_COMMENTS, False),
            # 管理员 据有所有权限，包括修改其他用户所属角色的权限
            'Administrator': (0xff, False)
        }
        for r in roles:
            role = Role.query.filter_by(name=r).first()
            if role is None:
                role = Role(name=r)
            role.permissions = roles[r][0]
            role.default = roles[r][1]
            db.session.add(role)
        db.session.commit()

    def has_permissions(self,perm):
        """
        检查角色权限
        :return False or True
        """
        return self.permissions & perm == perm

    def add_permissions(self,perm):
        """添加角色权限,如果角色没有这个权限则添加"""
        if not self.has_permissions(perm):
            self.permissions += perm

    def remove_permissions(self,perm):
        """删除角色权限"""
        if self.has_permissions(perm):
            self.permissions -= perm

    def reset_permissions(self):
        """重置权限 或 删除所有权限"""
        self.permissions = 0


    # 返回模型名称
    def __repr__(self):
        return '<Model Role %r>' % self.name


# 用户的数据模型
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    # 此列含索引,用户名
    username = db.Column(db.String(128), unique=True, index=True)
    # email地址
    email = db.Column(db.String(128), unique=True, index=True)
    # 存储加密后的用户密码值
    password_hash = db.Column(db.String(128))
    # role_id 字段是 roles 表的外键，代表了数据库的一种约束规则，表示role_id 的值必须存在与roles.id列中
    # 用来保证每个用户都有一个角色，每个角色能有多个用户
    role_id = db.Column(db.Integer, db.ForeignKey("roles.id"))
    # 用户注册账户确认与否标识 为 Boolean 字段
    confirmed = db.Column(db.Boolean,default=False)

    # 用户真实姓名
    name = db.Column(db.String(64))
    # 所在地
    location = db.Column(db.String(64))
    # 自我介绍 db.Text 不需要指定最大长度
    about_me = db.Column(db.Text())
    # 用户注册日期
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    # 最后一次登录时间
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)

    # 头像哈希
    avatar_hash = db.Column(db.String(32))

    # 帖子外键用于和用户的帖子关联
    posts = db.relationship('Post',backref='users',lazy='dynamic')


    # 实例初始化，赋予用户默认角色
    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)

        if self.role is None:
            # 如果用户邮箱为定义的管理员邮箱，则将用户角色设置为管理员
            if self.email in current_app.config['FLASKY_ADMIN']:
                self.role = Role.query.filter_by(permissions=0xff).first()
            # 如果角色为空，默认设置为用户角色
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()




    # 使用装饰器来处理密码
    @property
    def password(self):
        """@property 将函数当成成员变量来用"""
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        """获取散列后的密码值"""
        self.password_hash = generate_password_hash(password)

    def verify_password(self,password):
        """比对用户输入密码与用户注册的时加密后的面是否一致，一致返回正确"""
        return check_password_hash(self.password_hash,password)


    # 使用 flask-login 必须实现固定四个方法
    # 或者直接让用户模型继承 UserMixin类，默认实现下面四个方法
    def is_authenticated(self):
        """如果用户已经登录必须返回 TRUE"""
        return True

    def is_active(self):
        """如果循序用户登录，必须返回 TRUE"""
        return True

    def is_anonymous(self):
        """对普通用户必须返回 False"""
        return False

    def get_id(self):
        """必须返回用户的唯一表示符，使用 Unicode 编码字符串"""
        return self.id

    """
    itsdangerous 提供了多种生成令牌的方法。
    其中， TimedJSONWebSignatureSerializer 类生成具有过期时间的 JSON Web 签名（JSON Web Signatures，JWS）。
    这个类的构造函数接收的参数是一个密钥，在 Flask 程序中可使用 SECRET_KEY 设置。
    
    dumps() 方法为指定的数据生成一个加密签名，然后再对数据和签名进行序列化，生成令
    牌字符串。 expires_in 参数设置令牌的过期时间，单位为秒
    
    loads() 方法,其唯一的参数是令牌字符串。
    这个方法会检验签名和过期时间，如果通过，返回原始数据。
    如果提供给 loads() 方法的令牌不正确或过期了，则抛出异常。
    
    """
    def generate_confirmation_token(self,expiration = 3600):
        """定义生成令牌的方法，密令从配置中获取 目前配置的失效时间为一个小时"""
        s = Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'confirm': self.id })

    def confirm(self,token):
        """
        confirm() 方法检验令牌，如果检验通过，则吧新添加的confirmed 属性设为 True
        :param token:
        :return: True
        """
        s = Serializer(current_app.config['SECRET_KEY'])

        # 异常处理 获取令牌解码后的值
        try:
            data = s.loads(token)
        except:
            return False

        # 判断令牌的值是否与用户id一致
        if data.get('confirm') != self.id:
            logging.debug("conffirm value :{}".format(data.get('confirm')))
            return False

        self.confirmed = True
        logging.debug("models views in self.confirmed: {}".format( self.confirmed ))
        db.session.add(self)
        # 开始的时候是由于没有提交导致认证失败
        db.session.commit()
        return True

    def can(self,perm):
        """
        查看用户是否有指定权限
        :return 当用户角色不为空且权限与定义权限一致时返回 True 否则返回 FALSE
        """
        return self.role is not None and self.role.has_permissions(perm)

    def is_adminstrator(self):
        """检查管理员权限,因为经常使用所以单独实现"""
        return self.can(Permission.ADMINISTER)


    def ping(self):
        """修改用户最后一次登录时间"""
        self.last_seen = datetime.utcnow()
        db.session.add(self)




    def __repr__(self):
        return '<Model User %r>' % self.username


# 实现用户未登录时的current_user 的值
class AnonymousUser(AnonymousUserMixin):
    """
    对象继承 AnonymousUserMixin
    让程序不用先检查用户是否登录，就能调用 current_user.can() 和 current_user.is_administrator()
    我理解是用于未登录用户 或 匿名用户
    """
    def can(self,permissions):
        return False

    def is_adminstrator(self):
        return False


# 实例化未登录用户模型
login_manager.anonymous_user = AnonymousUser






# 用户帖子模型
class Post(db.Model):
    """Represents Proected posts."""
    __tablename__ = "posts"
    id = db.Column(db.String(64),primary_key = True)
    # 标题
    title = db.Column(db.String(255))
    # 文章内容
    text = db.Column(db.Text())
    # 发表时间
    publish_date = db.Column(db.DateTime)
    # Set the foreign key for Post
    # 用户id 外键
    user_id = db.Column(db.Integer,db.ForeignKey('users.id'))

    # def __init__(self,title):
    #     """初始化类方法"""
    #     self.title = title

    def __repr__(self):
        return "<Model Post '{}'>" .format(self.title)




# 实现 Flask-Login 要求实现的一个回调函数，使用指定标识加载用户
@login_manager.user_loader
def load_user(user_id):
    """
    加载用户的回调函数接收 Unicode 字符串形式表示的用户标示符
    如果能找到用户，这个函数必须返回用户对象，否则返回None
    """
    return User.query.get(int(user_id))

