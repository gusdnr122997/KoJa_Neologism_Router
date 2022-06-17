from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import relationship
from datetime import datetime
from sqlalchemy import ForeignKey

db = SQLAlchemy()
MAX_KEY_LENGTH = 200

class User(db.Model):
    __tablename__ = 'users'
    user_code = db.Column(db.Integer,primary_key=True,autoincrement=True)
    id = db.Column(db.String(64),unique=True,nullable=False)
    pw = db.Column(db.String(128),nullable=False)
    name = db.Column(db.String(64),nullable=False)
    email = db.Column(db.String(128),unique=True,nullable=False)
    create_at = db.Column(db.String(128), default=datetime.now().strftime("%Y-%m-%d"))
    last_login = db.Column(db.String(128), default=datetime.now().strftime("%Y-%m-%d"))

class Country(db.Model):
    __tablename__ = 'countries'
    code = db.Column(db.Integer,primary_key=True)
    name = db.Column(db.String(64))
    language = db.Column(db.String(64))

class Dic(db.Model):
    __tablename__ = 'dictionary'
    code = db.Column(db.Integer,primary_key=True,autoincrement=True)
    word = db.Column(db.String(64))
    meaning = db.Column(db.String)
    meaning_jp = db.Column(db.String)
    language_code = db.Column(db.Integer,ForeignKey('countries.code'))


class Similarity(db.Model):
    __tablename__ = 'similarity'
    src_word_code = db.Column(db.Integer,ForeignKey('dictionary.code'),primary_key=True)
    tar_word_code = db.Column(db.Integer,ForeignKey('dictionary.code'),primary_key=True)
    update_date = db.Column(db.String(128), default=datetime.now().strftime("%Y-%m-%d"))


class Vocab(db.Model):
    __tablename__ = 'vocab'
    user_code = db.Column(db.Integer,ForeignKey('users.user_code'),primary_key=True)
    word_code = db.Column(db.Integer,ForeignKey('dictionary.code'),primary_key=True)
    word = db.Column(db.String(64))
    meaning = db.Column(db.String)
    meaning_jp = db.Column(db.String)
    created_date = db.Column(db.String(128), default=datetime.now().strftime("%Y-%m-%d"))