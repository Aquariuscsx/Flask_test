from datetime import datetime

from app import db


class UserInfoTest(db.Model):
    __tablename__ = "user_info_test"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(50), unique=True)
    address = db.Column(db.String(100))

    # addtime=db.Column(db.DateTime)

    def __init__(self, username, email, address):
        self.username = username
        self.email = email
        self.address = address

    def __str__(self):
        return self.username


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    body = db.Column(db.Text)
    pub_date = db.Column(db.DateTime)
    flag = db.Column(db.Boolean, default=False)

    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    category = db.relationship('Category',
                               backref=db.backref('posts', lazy='dynamic'))

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date
        self.category = category

    def __repr__(self):
        return '<Post %r>' % self.title


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Category %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'
    uid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    pwd = db.Column(db.String(255))
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.Text)
    info = db.Column(db.String(255), unique=True)
    face = db.Column(db.String(255), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    uuid = db.Column(db.String(255), unique=True)

    def __repr__(self):
        return "<User %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class UserInfo(db.Model):
    __tablename__ = "user_info"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(100), unique=True)
    phone = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))

    def __repr__(self):
        return "<UserInfo_test %r>" % self.name


class Admin(db.Model):
    __tablename__ = "admin"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100),unique=True)
    pwd = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)

    def __repr__(self):
        return "<Admin %r>" % self.name

    def check_pwd(self, pwd):
        from werkzeug.security import check_password_hash
        return check_password_hash(self.pwd, pwd)


class Tag(db.Model):
    __tablename__ = "tag"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    addtime = db.Column(db.DateTime, index=True, default=datetime.now)


    def __repr__(self):
        return "<Tag %r>" % self.name



class Movie(db.Model):
   __tablename__ = "movie"
   id = db.Column(db.Integer, primary_key=True)  # 编号
   title = db.Column(db.String(255), unique=True)  # 标题
   url = db.Column(db.String(255), unique=True)  # url
   info = db.Column(db.Text)
   logo = db.Column(db.String(255), unique=True)  # logo
   star = db.Column(db.Integer)                   #星级
   playnum = db.Column(db.BigInteger)             #播放量
   commentnum = db.Column(db.BigInteger)          #评论数
   tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))  #外键，关联标签
   area = db.Column(db.String(255))                #上映地区
   release_time = db.Column(db.Date)               #上映时间
   length = db.Column(db.String(100))
   addtime = db.Column(db.DateTime, index=True, default=datetime.utcnow)


   def __repr__(self):
      return "<Movie %r>" % self.title