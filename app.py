from flask import Flask, jsonify
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/kahoot'

db.init_app(app)

# todo: use blueprint router
from usersRoutes import get_all_users, get_user_by_id, registration, update_user, delete_user
from quizzesRoutes import get_all_quizzess, get_quiz_by_id, create_quiz, update_quiz, delete_quiz
from questionsRoutes import get_all_questions, get_question_by_id, create_question, update_question, delete_question
from optionsRoutes import get_all_options

@app.route('/')
def main():
    return 'Test koneksi dulu coy'
