# -*- coding: utf-8 -*-
#
# Flaskフレームワークを使用した蔵書管理ツール
#
# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired, Email, Length


class BookForm(FlaskForm):
    name = StringField('Name', validators=[Length(
        min=-1, max=50, message='You cannot have more than 50 characters')])
    password = StringField('Password', validators=[Length(
        min=-1, max=50, message='You cannot have more than 50 characters')])

    isbn = StringField('ISBN', validators=[Length(
        min=-1, max=13, message='You cannot have more than 13 characters')])
    title = StringField('Title', validators=[DataRequired(), Length(
        min=-1, max=100, message='You cannot have more than 100 characters')])
    subtitle = StringField('Subtitle', validators=[Length(
        min=-1, max=100, message='You cannot have more than 100 characters')])
    author = StringField('Author', validators=[Length(
        min=-1, max=50, message='You cannot have more than 50 characters')])
    publisher = StringField('Publisher', validators=[Length(
        min=-1, max=50, message='You cannot have more than 50 characters')])
