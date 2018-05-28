from email import message

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError, EqualTo, Email, Regexp

from app.models import User

"""

"""


class LoginForm(FlaskForm):
    name = StringField(label="账号",
                       validators=[DataRequired("账号不能为空")],
                       description="账号",
                       render_kw={
                           "class": "form-control",
                           "placeholder": "请输入账号",
                       })
    pwd = PasswordField(label="密码",
                        validators=[DataRequired("密码不能为空")],
                        description="密码",
                        render_kw={
                            "class": "form-control",
                            "placeholder": "请输入密码",
                        }
                        )
    submit = SubmitField("登录",
                         render_kw={
                             "class": "btn btn-lg btn-success",

                         })







# class RegisterForm(FlaskForm):
#     name = StringField(label="昵称",
#                        validators=[DataRequired("麻烦请输入昵称信息")],
#                        description="昵称",
#                        render_kw={
#                            "class": "form-control input-lg",
#                            "placeholder": "请输入昵称",
#                        }
#                        )
#     email = StringField(label="邮箱",
#                         validators=[
#                             DataRequired("麻烦请输入邮箱信息"),
#                             Email("邮箱格式不正确！")
#                         ],
#                         description="邮箱",
#                         render_kw={
#                             "class": "form-control input-lg",
#                             "placeholder": "请输入邮箱",
#                         }
#                         )
#     phone = StringField(label="手机",
#                         validators=[
#                             DataRequired("麻烦请输入手机号码信息"),
#                             Regexp("1[3458]\\d{9}", message="手机格式不正确")
#                         ],
#                         description="手机",
#                         render_kw={
#                             "class": "form-control input-lg",
#                             "placeholder": "请输入手机号码",
#                         }
#                         )
#     pwd = PasswordField(label="密码",
#                         validators=[
#                             DataRequired("请输入密码信息"),
#
#                         ],
#                         description="密码",
#                         render_kw={
#                             "class": "form-control",
#                             "placeholder": "请输入密码",
#                         }
#                         )
#     repwd = PasswordField(label="确认密码",
#                           validators=[
#                               DataRequired("请输入确认密码信息"),
#                               EqualTo('pwd', message="两次密码输入不一致！")
#                           ],
#                           description="密码",
#                           render_kw={
#                               "class": "form-control",
#                               "placeholder": "请输入确认密码",
#                           }
#                           )
#     submit = SubmitField(
#         "注册",
#         render_kw={
#             "class": "btn btn-lg btn-success",
#         }
#     )
#
#     def validate_name(self, field):
#         name = field.data
#         user = User.query.filter_by(name=name).count()
#         if user == 1:
#             raise ValidationError("昵称已经存在!")
#
#     def validate_email(self, field):
#         email = field.data
#         user = User.query.filter_by(email=email).count()
#         if user == 1:
#             raise ValidationError("邮箱已经存在!")
#
#     def validate_phone(self, field):
#         phone = field.data
#         user = User.query.filter_by(phone=phone).count()
#         if user == 1:
#             raise ValidationError("手机已经存在!")
"""

用户名:name
邮箱:email
手机:phone
密码:pwd
确认密码:repwd
"""


class RegisterForm(FlaskForm):
    name = StringField(label="用户名",
                       validators=[DataRequired("请输入非空用户名")],
                       description="帐户",
                       render_kw={
                           "class": "form-control",
                           "placeholder": "请输入用户名"}
                       )
    email = StringField(label="邮箱",
                        validators=[DataRequired("请输入非空邮箱"),
                                    Email("请输入正确email格式")],
                        description="邮箱",
                        render_kw={
                            "class":"form-control",
                            "placeholder":"请输入邮箱"
                        })
    phone = StringField(label="手机号",
                        validators=[DataRequired("请输入非空手机号"),
                                    Regexp("1[356789]\\d{9}",message="手机格式不正确")],
                        description="手机号",
                        render_kw={
                            "class":"form-control",
                            "placeholder": "请输入手机号"
                        })

    pwd = PasswordField(label="密码",
                        validators=[DataRequired("密码不能为空")],
                        description="密码",
                        render_kw={
                            "class":"form-control",
                            "placeholder": "请输入密码"
                        })
    repwd = PasswordField(label="确认密码",
                        validators=[DataRequired("确认密码不能为空"),
                                    EqualTo("pwd", "两次密码输入不一致")],
                        description="确认密码",
                        render_kw={
                            "class": "form-control",
                            "placeholder": "请再次输入密码"
                        })
    submit = SubmitField("注册",
                         render_kw={
                             "class":"btn btn-lg btn-success"
                         })

    def validate_name(self,field):
        name = field.data
        user_count = User.query.filter_by(name=name).count()
        if user_count == 1:
            raise ValidationError("该昵称已存在!!")

    def validate_email(self,field):
        email = field.data
        user_count = User.query.filter_by(email=email).count()
        if user_count == 1:
            raise ValidationError("该邮箱已存在!")

    def validate_phone(self,field):
        phone = field.data
        user_count = User.query.filter_by(phone=phone).count()
        if user_count == 1:
            raise ValidationError("该手机号已注册!")



