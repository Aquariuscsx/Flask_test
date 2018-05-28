from functools import wraps

from flask import Response, render_template, url_for, redirect, flash, session, request

from werkzeug.security import generate_password_hash

from . import home


def check_user_login(func):
  @wraps(func)
  def decorated_function(*args, **kwargs):
    if "user" not in session:
      return redirect(url_for("home.home_login", next=request.url))
    return func(*args, **kwargs)
  return decorated_function


@home.route("/test/")
@check_user_login
def mtest():
  return Response("this is the function.")


@home.route("/index/")
def home_index():
  return render_template("home/index.html")


@home.route('/')
def index():
    login_flag = 0
    user_name = ''
    if session.get('user'):
        login_flag = 1
        user_name = session['user']
    return render_template("home/index.html", login_flag=login_flag, username=user_name)


@home.route('/login_test/')
def home_login_test():
    from app.models import UserInfo
    user_list = UserInfo.query.all()
    return render_template("home/login_test.html", user_list=user_list)


@home.route("/add_user/<string:username>/<string:email>/<string:address>/")
def home_add_user(username, email, address):
    # 传入Model层， 存储数据库
    from app import db
    from app.models import UserInfo
    user = UserInfo(username=username, email=email, address=address)
    db.session.add(user)
    db.session.commit()
    print('save ok.')
    import json
    data = {'username': username, 'email': email, 'address': address}
    result = {'code': 200, 'message': 'ok', 'data': data}
    return Response(json.dumps(result))


@home.route("/add_category/<string:name>/")
def add_category(name):
    from app import db
    from app.models import Category
    cate = Category(name=name)
    db.session.add(cate)
    db.session.commit()
    import json
    data = {'name': 'name'}
    result = {"state": 200, "msg": 'ok', "data": data}
    return Response(json.dumps(result))


@home.route("/login/", methods=['POST','GET'])
def home_login():
    from app.home.forms import LoginForm
    from app import db
    from app.models import User
    form = LoginForm()
    print('11111111')
    if form.validate_on_submit():
        print('2222222')
        data = form.data
        user = User.query.filter_by(name=data["name"]).first()
        if user:
            if not user.check_pwd(data["pwd"]):
                flash("密码验证错误", "err")
                return redirect(url_for("home.home_login"))
        else:
            flash("用户不存在", "err")
            return redirect(url_for("home.home_login"))
        session["user"] = user.name
        session["user_id"] = user.uid


        return redirect(url_for("home.index"))

    return render_template('home/login.html',title="会员登录", form=form)


@home.route("/vip_login/")
def login():
    return render_template("home/vip_login.html")


@home.route("/wflogin/")
def home_wflogin():
    from .forms import LoginForm
    form_login = LoginForm()
    return render_template("home/wflogin.html", form_login=form_login)


@home.route("/logout/")
def home_logout():
    session.pop("name", None)
    session.pop("uid", None)
    return redirect(url_for("home.home_login"))


@home.route("/register/", methods=[ 'GET','POST'])
def home_register():
    from app import db
    from app.home.forms import RegisterForm
    from app.models import User
    form = RegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = User(name=data["name"],email=data["email"],phone=data["phone"],pwd=generate_password_hash(data["pwd"]))
        db.session.add(user)
        db.session.commit()
        flash("恭喜!注册成功", "ok")
    return render_template("home/register.html", form=form)


@home.route("/wf_register/")
def home_wf_register():
    from .forms import RegisterForm
    form = RegisterForm()
    return render_template("home/wf_register.html", form=form)


@home.route("/animation/")
def animation():
    return render_template("home/animation.html")


@home.route("/play/")
def play():
    return render_template("home/play.html")
