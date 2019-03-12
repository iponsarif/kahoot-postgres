from flask import Flask, jsonify
from models import db

app = Flask(__name__)

app.config['JSON_SORT_KEYS'] = False

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/kahoot'

db.init_app(app)

# todo: use blueprint router
from usersRoutes import get_all_users
from quizzesRoutes import get_all_quizzess
from questionsRoutes import get_all_questions
from optionsRoutes import get_all_options
from gamesRoutes import get_all_games

@app.route('/')
def main():
    return 'Test koneksi dulu coy'