#coding=utf-8
from flask_wtf import Form
from wtforms import validators, SubmitField, StringField, PasswordField
from wtforms.validators import Required

class LoginForm(Form):
    username = StringField('用户名', validators=[Required()])
    password = PasswordField('密码', validators=[Required()])
    submit = SubmitField('登录')
