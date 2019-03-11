import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String())
    password = db.Column(db.String())
    fullname = db.Column(db.String())
    email = db.Column(db.String())
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, username, password, fullname, email):
        self.username = username
        self.password = password
        self.fullname = fullname
        self.email = email
    
    def __repr__(self):
        return '<user id ()>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password,
            'fullname': self.fullname,
            'email': self.email,
            'created_at': self.created_at
        }

class Quizzess(db.Model):
    __tablename__ = 'quizzess'

    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer())
    title = db.Column(db.String())
    category = db.Column(db.String())

    def __init__(self, creator_id, title, category):
        self.creator_id = creator_id
        self.title = title
        self.category = category
    
    def __repr__(self):
        return '<quiz id ()>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'creator_id': self.creator_id,
            'title': self.title,
            'category': self.category,
        }

class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer())
    question = db.Column(db.String())
    number = db.Column(db.Integer())
    answer = db.Column(db.String())

    def __init__(self, quiz_id, question, number, answer):
        self.quiz_id = quiz_id
        self.question = question
        self.number = number
        self.answer = answer
    
    def __repr__(self):
        return '<question id ()>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question': self.question,
            'number': self.number,
            'answer': self.answer
        }

class Options(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer())
    option = db.Column(db.String())
    detail = db.Column(db.Integer())

    def __init__(self, question_id, option, detail):
        self.question_id = question_id
        self.option = option
        self.detail = detail
    
    def __repr__(self):
        return '<option id ()>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'option': self.option,
            'detail': self.detail,
        }        