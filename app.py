# -*- coding: utf-8 -*-
#
# Flaskフレームワークを使用した蔵書管理ツール
#
# Copyright (c) 2018 YA-androidapp(https://github.com/YA-androidapp) All rights reserved.

from flask import Flask, redirect, url_for, render_template, request, flash, jsonify
from models import db, Book, User
from forms import BookForm

import traceback

# API呼び出しに使用
import urllib.request
import xml.etree.ElementTree as ET

# Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret-key'
app.config['DEBUG'] = True

# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///book.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)


@app.route("/")
def index():
    '''
    Home page
    '''
    return redirect(url_for('books'))


@app.route("/new_book", methods=('GET', 'POST'))
def new_book():
    '''
    Create new book
    '''
    form = BookForm()
    if form.validate_on_submit():

        # TODO
        isbn = request.form['isbn']
        name = request.form['name']
        book_db = db.session.query(Book).filter_by(isbn=isbn)
        user_db = db.session.query(User).filter_by(
            name=name).first()
        if book_db is None:
            if user_db is not None:
                pw_db = user_db.password
                pw_in = request.form['password']
                print(name)
                print(pw_db)
                print(pw_in)
                if pw_db == pw_db:
                    # db.session.add(user)
                    user = User.query.filter_by(name=name).first()
                    print(user.name)
                    #
                    my_book = Book()
                    form.populate_obj(my_book)
                    try:
                        db.session.add(my_book)
                        user.books.append(my_book)
                        db.session.commit()
                        # User info
                        flash('Book created correctly', 'success')
                        # return redirect(url_for('books'))
                        return redirect(url_for('new_book'))
                    except:
                        db.session.rollback()
                        flash('Error generating book.', 'danger')
                        # flash(traceback.format_exc(), 'danger')

    return render_template('web/new_book.html', form=form)


@app.route("/search_api/", methods=('GET', 'POST'))
def search_api_empty():
    response = jsonify(status=-1)
    response.status_code = 200
    return response


@app.route("/search_api/<isbn>", methods=('GET', 'POST'))
def search_api(isbn):
    '''
    Search book using the API

    :param isbn: ISBN
    '''
    isbn = isbn.replace('-', '').replace(' ', '')
    # print(isbn)
    if isbn.isdigit() and len(isbn) == 13:
        try:
            url = 'http://iss.ndl.go.jp/api/sru?operation=searchRetrieve&query=isbn=' + isbn
            print(url)
            headers = {
                "User-Agent":  "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:50.0) Gecko/20000101 Firefox/50.0"}
            req = urllib.request.Request(url, None, headers)
            with urllib.request.urlopen(req) as response:
                xml = response.read().decode(response.headers.get_content_charset())
                xml = xml.replace('&lt;', '<').replace('&gt;', '>').replace(
                    '&apos;', '\'').replace('&quot;', '"').replace('&amp;', '&')
                print(xml)
                root = ET.fromstring(xml)
                title = root.find(
                    ".//{http://purl.org/dc/elements/1.1/}title").text
                creator = root.find(
                    ".//{http://purl.org/dc/elements/1.1/}creator").text
                publishers = []
                for k in root.findall(".//{http://purl.org/dc/elements/1.1/}publisher"):
                    publishers.append(k.text)

                list = [
                    dict(creator=creator, id=1,
                         publishers=publishers, status=0, title=title)
                ]
                response = jsonify(results=list)
                response.status_code = 200
                return response
        except:
            # response = jsonify(status=str(traceback.format_exc()))
            response = jsonify(status=-1)
            response.status_code = 200
            return response


@app.route("/edit_book/<isbn>", methods=('GET', 'POST'))
def edit_book(isbn):
    '''
    Edit book

    :param isbn: ISBN
    '''
    my_book = Book.query.filter_by(isbn=isbn).first()
    form = BookForm(obj=my_book)
    if form.validate_on_submit():
        try:
            form.populate_obj(my_book)
            db.session.add(my_book)
            db.session.commit()
            flash('Saved successfully', 'success')
        except:
            db.session.rollback()
            flash('Error update book.', 'danger')
    return render_template(
        'web/edit_book.html',
        form=form)


@app.route("/books")
def books():
    '''
    Show alls books
    '''
    books = Book.query.order_by(Book.title).all()
    return render_template('web/books.html', books=books)


@app.route("/search")
def search():
    '''
    Search
    '''
    title_search = request.args.get('title')
    all_books = Book.query.filter(
        Book.title.contains(title_search)
    ).order_by(Book.title).all()
    return render_template('web/books.html', books=all_books)


@app.route("/books/delete", methods=('POST',))
def books_delete():
    '''
    Delete book
    '''
    try:
        mi_book = Book.query.filter_by(isbn=request.form['isbn']).first()
        db.session.delete(mi_book)
        db.session.commit()
        flash('Delete successfully.', 'danger')
    except:
        db.session.rollback()
        flash('Error delete  book.', 'danger')

    return redirect(url_for('books'))


if __name__ == "__main__":
    app.run()
