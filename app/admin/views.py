import os
from functools import wraps

from flask import render_template, redirect, url_for, flash, session, request

from . import admin


def check_admin_login(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("admin.login", next=request.url))
        return func(*args, **kwargs)

    return decorated_function


@admin.route("/")
def index():
    return render_template("admin/admin.html")


@admin.route("/index/")
def admin_index():
    from datetime import datetime
    login_flag = 0
    user_name = ''
    if session.get('admin'):
        login_flag = 1
        user_name = session['admin']
        utcnow = datetime.utcnow()
    return render_template("admin/index.html", login_flag=login_flag, username=user_name, utcnow=utcnow)


@admin.route("/login/", methods=["GET", "POST"])
def login():
    from app.admin.forms import AdminLoginForm
    from app.models import Admin
    form = AdminLoginForm()
    if form.validate_on_submit():
        data = form.data
        admin = Admin.query.filter_by(name=data['account']).first()
        if not admin.check_pwd(data['pwd']):
            flash("密码错误", "err")
            return redirect(url_for("admin.login"))
        session["admin"] = data['account']
        return redirect(url_for("admin.admin_index"))
    return render_template("admin/login.html", form=form)


@admin.route("/logout/")
def logout():
    session.pop("admin", None)
    return redirect(url_for("admin.login"))


@admin.route("/register/", methods=["GET", "POST"])
def register():
    from werkzeug.security import generate_password_hash
    from app.admin.forms import AdminRegisterForm
    from app.models import Admin
    from app import db
    form = AdminRegisterForm()
    if form.validate_on_submit():
        data = form.data
        user = Admin(
            name=data['name'],
            pwd=generate_password_hash(data['pwd']),
        )
        db.session.add(user)
        db.session.commit()
        flash("恭喜，管理员注册成功！", "ok")
    return render_template("admin/register.html", title="会员注册", form=form)


@admin.route("/tag/add/", methods=["GET", "POST"])
@check_admin_login
def tag_add():
    from app.admin.forms import TagForm
    from app.models import Tag
    from app import db
    form = TagForm()
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data["name"]).count()
        if tag_count == 1:
            flash("标签名已经存在", "err")
            return redirect(url_for('admin.tag_add'))
        tag = Tag(name=data['name'])
        db.session.add(tag)
        db.session.commit()
        flash("标签添加成功!", "ok")
    return render_template("admin/tag_add.html", form=form)


@admin.route("/tag/list/<int:page>/", methods=["GET"])
@check_admin_login
def tag_list(page):
    from app.models import Tag
    if page is None:
        page = 1
    page_data = Tag.query.order_by(Tag.addtime.asc()).paginate(page=page, per_page=5)
    return render_template("admin/tag_list.html", page_data=page_data)


@admin.route("/tag/del/<int:id>/", methods=["GET"])
@check_admin_login
def tag_del(id=None):
    from app.models import Tag
    from app import db
    tag = Tag.query.filter_by(id=id).first_or_404()
    db.session.delete(tag)

    db.session.commit()
    flash("删除标签成功", "ok")
    return redirect(url_for("admin.tag_list", page=1))


@admin.route("/tag/edit/<int:id>", methods=["GET", "POST"])
@check_admin_login
def tag_edit(id=None):
    from app.admin.forms import TagForm
    from app.models import Tag
    from app import db
    form = TagForm()
    tag = Tag.query.get_or_404(id)
    if form.validate_on_submit():
        data = form.data
        tag_count = Tag.query.filter_by(name=data['name']).count()
        if tag.name != data['name'] and tag_count == 1:
            flash("标签已经存在", "err")
            return redirect(url_for("admin.tag_edit", id=id))
        # 入库
        tag.name = data["name"]
        db.session.add(tag)
        db.session.commit()
        flash("修改标签成功", "ok")
        return redirect(url_for("admin.tag_edit", id=id))
    return render_template("admin/tag_edit.html", form=form, tag=tag)


def change_filename(filename):
    import os, uuid
    from datetime import datetime
    fileinfo = os.path.splitext(filename)
    filename = datetime.now().strftime("%Y%m%d%H%M%S") + str(uuid.uuid4().hex) + fileinfo[-1]
    return filename


@admin.route("/movie/add/", methods=["GET", "POST"])
@check_admin_login
def movie_add():
    from app.admin.forms import MovieForm
    from app.models import Movie
    from app import db, app
    from werkzeug.utils import secure_filename
    form = MovieForm()
    if form.validate_on_submit():
        data = form.data
        # 上传文件
        file_url = secure_filename(form.url.data.filename)
        file_logo = secure_filename(form.logo.data.filename)
        # 自动创建上传文件
        if not os.path.exists(app.config["UP_DIR"]):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")

        url = change_filename(file_url)
        logo = change_filename(file_logo)
        form.url.data.save(app.config["UP_DIR"] + url)
        form.logo.data.save(app.config["UP_DIR"] + logo)
        movie = Movie(
            title=data['title'],
            url=url,
            info=data['info'],
            logo=logo,
            star=int(data['star']),
            playnum=0,
            commentnum=0,
            tag_id=int(data['tag_id']),
            area=data['area'],
            release_time=data['release_time'],
            length=data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功", "ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("admin/movie_add.html", form=form)


@admin.route("/movie/list/<int:page>", methods=["GET", "POST"])
@check_admin_login
def movie_list(page=None):
    from app.models import Movie, Tag
    if page is None:
        page = 1
    pages = Movie.query.join(Tag).filter(
        Tag.id == Movie.tag_id  # 表进行关联
    ).order_by(
        Movie.addtime.desc()  # 按照创建时间进行倒序排序
    )
    page_data = pages.paginate(page=page, per_page=5)
    return render_template("admin/movie_list.html", page_data=page_data)


@admin.route("/movie/del/<int:mid>/", methods=["POST", "GET"])
@check_admin_login
def movie_del(mid=None):
   from app.models import Movie
   from app import db
   movie = Movie.query.get_or_404(int(mid))
   db.session.delete(movie)
   db.session.commit()
   flash("删除电影成功！", "ok")
   return redirect(url_for("admin.movie_list", page=1))