from flask import request, json, jsonify

from app import app
from models import db, Quizzess, Questions

# get all quizzess
@app.route('/quiz/getAllQuizzess', methods=['GET'])
def get_all_quizzess():
    try:
        username = request.cookies.get('username')
        print('username',username)
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

@app.route('/quiz/getQuizByCreatorId/<creator_id_>', methods=['GET'])
def get_quiz_by_creator_id(creator_id_):
    try:
        username = request.cookies.get('username')
        print('username',username)
        quizzess = Quizzess.query.order_by(Quizzess.id).filter_by(creator_id=creator_id_).all()
        return jsonify([quiz.serialize() for quiz in quizzess])
    except Exception as e:
        return(str(e))

# create quiz
@app.route('/quiz/createQuiz', methods=['POST'])
def create_quiz():
    response = {}
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
        quiz = Quizzess.query.filter_by(creator_id=creator_id, title=title, category=category).first()
        response['message'] = "Create quiz success"
        response['id'] = quiz.id
        return jsonify(response), 200
    except Exception as e:
        response['message'] = str(e)
        return jsonify(response), 400

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