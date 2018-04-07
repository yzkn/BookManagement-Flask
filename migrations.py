# -*- coding: utf-8 -*-
#
# Flaskフレームワークを使用した蔵書管理ツール
#
# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from models import db, User  # , Book
# from faker import Factory
# import random

db.drop_all()
db.create_all()

# fake = Factory.create()
# for num in range(100):
#     fullname = fake.name().split()

#     user = User(name=fake.name(), password="password")
#     db.session.add(user)

#     isbn = random.randint(0, 9999999999999)
#     title = fullname[0]
#     subtitle = ' '.join(fullname[1:])
#     author = fake.name()
#     publisher = fake.name()+fake.name()

#     mi_book = Book(isbn=isbn, title=title, subtitle=subtitle,
#                    author=author, publisher=publisher)
#     db.session.add(mi_book)
#     user.books.append(mi_book)
#     db.session.commit()

name = 'user1'
password = "password"
user = User(name=name, password=password)
db.session.add(user)
db.session.commit()
