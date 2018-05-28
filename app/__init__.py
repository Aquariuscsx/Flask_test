from flask import Flask, render_template
from app.admin import admin as admin_blueprint
from app.home import home as home_blueprint

app = Flask(__name__)

app.register_blueprint(admin_blueprint, url_prefix="/admin")
app.register_blueprint(home_blueprint, url_prefix="/home")

from flask_sqlalchemy import SQLAlchemy

mysql_coon_str = \
    "mysql+pymysql://root:123456@192.168.51.13:3306/Flask?charset=utf8"
app.config['SQLALCHEMY_DATABASE_URI'] = mysql_coon_str
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = True

app.config['SECRET_KEY'] = "12345678"


db = SQLAlchemy(app)

from app import models


@app.route("/")
def index():
    return render_template("home/index.html")

