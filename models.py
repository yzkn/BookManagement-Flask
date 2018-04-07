# -*- coding: utf-8 -*-
#
# Flaskフレームワークを使用した蔵書管理ツール
#
# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

user_book_table = db.Table('user_books',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id')),
    db.Column('book_id', db.Integer, db.ForeignKey('books.isbn')))


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)
    password = db.Column(db.Text, nullable=False)

    books = db.relationship('Book', order_by='Book.isbn',
        uselist=True, backref='users',
        secondary=user_book_table)

    def __repr__(self):
        return '<Users %r>' % self.name


class Book(db.Model):
    __tablename__ = 'books'

    isbn = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.Text, nullable=True)
    author = db.Column(db.Text, nullable=True, unique=True)
    publisher = db.Column(db.Text, nullable=True, unique=False)

    def __repr__(self):
        return '<Books %r>' % self.title
