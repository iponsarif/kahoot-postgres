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
        }