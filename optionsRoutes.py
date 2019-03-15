from flask import request, json, jsonify

from models import db, Questions, Options 
from app import app

@app.route('/question/<id_>/getAllOptions', methods=['GET'])
def get_all_options(id_):
    try:
        options = Questions.query.join(Options, Questions.id==Options.question_id).filter(Questions.id==id_).all()
        return jsonify([opt.serialize() for opt in options])
    except Exception as e:
        return(str(e))

# get question by id
@app.route('/question/getOption/<id_>', methods=['GET'])
def get_option_by_id(id_):
    try:
        option = Options.query.filter_by(id=id_).first()
        return jsonify(option.serialize())
    except Exception as e:
        return(str(e))

# create option
@app.route('/question/<question_id_>/createOption', methods=['POST'])
def create_option(question_id_):
    question_id_ = question_id_
    body = request.json

    a = body['a']
    b = body['b']
    c = body['c']
    d = body['d']

    try:
        option = Options( 
            question_id = question_id_,
            a = a,
            b = b,
            c = c,
            d = d
            )
        db.session.add(option)
        db.session.commit()
        return 'Option added, option id ={}'.format(option.id)
    except Exception as e:
        return(str(e))

# update option
@app.route('/questions/updateOption/<id_>', methods=['POST'])
def update_option(id_):
    # ngambil dulu data option yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    option = get_option_by_id(id_).json 
    body = request.json

    a = body['a']
    b = body['b']
    c = body['c']
    d = body['d']

    # kalau yg diupdate tidak semua kolom
    if a is None:
        a = option['a']

    if b is None:
        b = option['b']
    
    if c is None:
        c = option['c']

    if d is None:
        d = option['d']
        
    try:
        option_ = {
            'a': a,
            'b': b,
            'c': c,
            'd': d
        }
        
        db.session.query(Options).filter_by(id=id_).update(option_)
        db.session.commit()
        return 'Question updated, question id ={}'.format(id_)
    except Exception as e:
        return(str(e))

# hard delete option by id
@app.route('/questions/deleteOption/<id_>', methods=['DELETE'])
def delete_option(id_): 
    try:
        option = Options.query.filter_by(id=id_).first()
        db.session.delete(option)
        db.session.commit()
        return 'Option deleted, option id={}'.format(id_)
    except Exception as e:
        return(str(e))