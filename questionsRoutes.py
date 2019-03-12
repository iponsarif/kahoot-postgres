from flask import request, json, jsonify

from models import Questions, Quizzess, Options
from app import app
from models import db

@app.route('/getAllQuestions', methods=['GET'])
def get_all_questions():
    try:
        questions = Questions.query.all()
        return jsonify([quest.serialize() for quest in questions])
    except Exception as e:
        return(str(e))

# get question by id
@app.route('/getQuestion/<id_>', methods=['GET'])
def get_question_by_id(id_):
    try:
        question = Questions.query.filter_by(id=id_).first()
        return jsonify(question.serialize())
    except Exception as e:
        return(str(e))

# create question
@app.route('/quiz/<quiz_id_>/createQuestion', methods=['POST'])
def create_question(quiz_id_):
    body = request.json
    question = body['question']
    number = body['number']
    answer = body['answer']
    option = body['options']
    a = option["a"]
    b = option["b"]
    c = option["c"]
    d = option["d"]
    # option_list = []
    try:
        question = Questions(
            quiz_id = quiz_id_,
            question = question,
            number = number,
            answer = answer
            )

        # option_list.append(Options(Questions.id,a,b,c,d))

        question.options = [Options(Questions.id,a,b,c,d)]
        db.session.add(question)
        db.session.commit()
        return 'Question added, question id ={}'.format(question.id)
    except Exception as e:
        return(str(e))

@app.route('/quiz/updateQuestion/<id_>', methods=['POST'])
def update_question(id_):
    # ngambil dulu data quiz yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    _question = get_question_by_id(id_).json 
    
    question = request.args.get('question')
    number = request.args.get('number')
    answer = request.args.get('answer')

    # kalau yg diupdate tidak semua kolom
    if question is None:
        question = _question['question']

    if number is None:
        number = _question['number']

    if answer is None:
        answer = _question['answer']
        
    try:
        question_ = {
            'question': question,
            'number': number,
            'answer': answer
        }
        
        db.session.query(Questions).filter_by(id=id_).update(question_)
        db.session.commit()
        return 'Question updated, question id ={}'.format(id_)
    except Exception as e:
        return(str(e))

# hard delete question by id
@app.route('/quiz/deleteQuestion/<id_>', methods=['DELETE'])
def delete_question(id_):
    try:
        question = Questions.query.filter_by(id=id_).first()
        db.session.delete(question)
        db.session.commit()        

        return 'Question deleted, question id={}'.format(id_)
    except Exception as e:
        return(str(e))