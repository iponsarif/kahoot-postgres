from flask import request, json, jsonify
from random import randint

from models import db, Games, Leaderboards, Questions, Quizzess
from app import app

# get All Games
@app.route('/getAllGames', methods=['GET'])
def get_all_games():
    try:
        games = Games.query.order_by(Games.quiz_id).all()
        return jsonify([game.serialize() for game in games])
    except Exception as e:
        return(str(e))

# create game
@app.route('/createGame', methods=['POST'])
def create_game():    
    
    # if game_pin sudah ada
    game_pin = randint(100000,999999)
    quiz_id = request.args.get('quiz_id')

    try:
        game = Games( 
            game_pin = game_pin,
            quiz_id = quiz_id
        )
        db.session.add(game)
        db.session.commit()
        return 'Game created, game pin = {}'.format(game.game_pin)
    except Exception as e:
        return(str(e))

# join game
@app.route('/joinGame', methods=['POST'])
def join_game():
    game_pin = request.args.get('game_pin')
    participant = request.args.get('username')
    score = 0

    try:
        leaderboard = Leaderboards(
            game_pin = game_pin,
            participant = participant,
            score = score
        )
        db.session.add(leaderboard)
        db.session.commit()
        return '{} joined to game pin {}'.format(leaderboard.participant, leaderboard.game_pin)
    except Exception as e:
        return(str(e))

# get leaderboard
@app.route('/leaderboard/<game_pin_>', methods=['GET'])
def get_leaderboard_by_game_pin(game_pin_):
    try:
        leaderboard = Leaderboards.query.filter_by(game_pin=game_pin_).order_by(Leaderboards.score.desc()).all()
        return jsonify([board.serialize() for board in leaderboard])
    except Exception as e:
        return(str(e))

# answer
@app.route('/answerGame/<game_pin_>', methods=['POST'])
def submit_answer(game_pin_):
    # quiz_id_ = request.args.get('quiz_id')
    number_ = request.args.get('question_number')
    username_ = request.args.get('username')
    answer_ = request.args.get('answer')
    
    # nyari quiz_id
    try:
        game = Games.query.filter_by(game_pin=game_pin_).first()
        quiz_id_ = game.quiz_id
    except Exception as e:
        return str(e)
    
    # nyari answer di database
    try:
        question = Questions.query.join(Quizzess, Quizzess.id==Questions.quiz_id).filter(Questions.quiz_id==quiz_id_, Questions.number==number_).first()

        answer = question.answer
    except Exception as e:
        return(str(e))

    # nyari score (sebelum ditambah kalau benar)
    try:
        leaderboard = Leaderboards.query.filter_by(game_pin=game_pin_, participant=username_).first()
        score = leaderboard.score
    except Exception as e:
        return(str(e))

    # kalau jawaban benar
    if answer == answer_:
        score += 100

    #
    try:
        leaderboard = {
            'game_pin': game_pin_,
            'participant': username_,
            'score': score
        }
        db.session.query(Leaderboards).filter(Leaderboards.game_pin==game_pin_, Leaderboards.participant==username_).update(leaderboard)
        db.session.commit()
        return 'Correct answer, your score is {}'.format(leaderboard['score'])
    except Exception as e:
        return(str(e))