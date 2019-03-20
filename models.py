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
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    title = db.Column(db.String())
    category = db.Column(db.String())
    questions = db.relationship('Questions', cascade="all,delete", backref='quizzess', lazy=True)
    created_at = db.Column(db.DateTime, default=datetime.datetime.now())

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
            'question-list': [{'number': item.number, 'question': item.question, 'answer': item.answer, 'qs_id': item.id} for item in self.questions]
        }

class Questions(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzess.id'))
    question = db.Column(db.String())
    number = db.Column(db.Integer)
    answer = db.Column(db.String())
    options = db.relationship('Options', cascade="all,delete", backref='questions', lazy=True)

    def __init__(self, quiz_id, question, number, answer):
        self.quiz_id = quiz_id
        self.question = question
        self.number = number
        self.answer = answer
    
    def __repr__(self):
        return '<question id ()>'.format(self.id)

    def serialize(self):
        quiz = Quizzess.query.filter(Quizzess.id==self.quiz_id).first()
        return {
            'quiz': quiz.title,
            'id': self.id,
            'quiz_id': self.quiz_id,
            'question': self.question,
            'number': self.number,
            'answer': self.answer,
            'options': [{'a':item.a, 'b':item.b, 'c':item.c, 'd':item.d} for item in self.options]
        }

class Options(db.Model):
    __tablename__ = 'options'

    id = db.Column(db.Integer, primary_key=True)
    question_id = db.Column(db.Integer(), db.ForeignKey('questions.id'))
    a = db.Column(db.String())
    b = db.Column(db.String())
    c = db.Column(db.String())
    d = db.Column(db.String())

    def __init__(self, question_id, a, b, c, d):
        self.question_id = question_id
        self.a = a
        self.b = b
        self.c = c
        self.d = d
    
    def __repr__(self):
        return '<option id ()>'.format(self.id)

    def serialize(self):
        return {
            'id': self.id,
            'question_id': self.question_id,
            'a': self.a,
            'b': self.b,
            'c': self.c,
            'd': self.d,
        }        

class Games(db.Model):
    __tablename__ = 'games'

    game_pin = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey('quizzess.id'))

    def __init__(self, game_pin, quiz_id):
        self.game_pin = game_pin
        self.quiz_id = quiz_id
    
    def __repr__(self):
        return '<game pin ()>'.format(self.game_pin)

    def serialize(self):
        return {
            'game_pin': self.game_pin,
            'quiz_id': self.quiz_id
        }

class Leaderboards(db.Model):
    __tablename__ = 'leaderboards'

    game_pin = db.Column(db.Integer, db.ForeignKey('games.game_pin'))
    participant = db.Column(db.String(), primary_key=True)
    score = db.Column(db.Integer, default=0)

    def __init__(self, game_pin, participant, score):
        self.game_pin = game_pin
        self.participant = participant
        self.score = score
    
    def serialize(self):
        return {
            # 'game_pin': self.game_pin,
            'username': self.participant,
            'score': self.score
        }    