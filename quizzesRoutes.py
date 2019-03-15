from flask import request, json, jsonify

from app import app
from models import db, Quizzess, Questions

# get all quizzess
@app.route('/quiz/getAllQuizzess', methods=['GET'])
def get_all_quizzess():
    try:
        quizzess = Quizzess.query.order_by(Quizzess.id).all()
        return jsonify([quiz.serialize() for quiz in quizzess])
    except Exception as e:
        return(str(e))

# get quiz by id
@app.route('/quiz/getQuiz/<id_>', methods=['GET'])
def get_quiz_by_id(id_):
    try:
        quiz = Quizzess.query.filter_by(id=id_).first()
        return jsonify(quiz.serialize())
    except Exception as e:
        return(str(e))

# create quiz
@app.route('/quiz/createQuiz', methods=['POST'])
def create_quiz():
    body = request.json

    creator_id = body['creator_id']
    title = body['title']
    category = body['category']

    try:
        quiz = Quizzess(
            creator_id = creator_id,
            title = title,
            category = category
            )
        db.session.add(quiz)
        db.session.commit()
        return 'Quiz added, quiz id ={}'.format(quiz.id)
    except Exception as e:
        return(str(e))

# update quiz by quiz.id
@app.route('/quiz/updateQuiz/<id_>', methods=['POST'])
def update_quiz(id_):
    # ngambil dulu data quiz yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    quiz = get_quiz_by_id(id_).json 
    body = request.json

    creator_id = body['creator_id']
    title = body['title']
    category = body['category']

    # kalau yg diupdate tidak semua kolom
    if creator_id is None:
        creator_id = quiz['creator_id']

    if title is None:
        title = quiz['title']

    if category is None:
        category = quiz['category']
        
    try:
        quiz_ = {
            'creator_id': creator_id,
            'title': title,
            'category': category
        }
        
        db.session.query(Quizzess).filter_by(id=id_).update(quiz_)
        db.session.commit()
        return 'Quiz updated, quiz id ={}'.format(id_)
    except Exception as e:
        return(str(e))

# hard delete quiz by id
@app.route('/quiz/deleteQuiz/<id_>', methods=['DELETE'])
def delete_quiz(id_):
    try:
        quiz = Quizzess.query.filter_by(id=id_).first()
        db.session.delete(quiz)
        db.session.commit()
        return 'Quiz deleted, quiz id={}'.format(id_)
    except Exception as e:
        return(str(e))