from flask import Flask, jsonify
from models import db

app = Flask(__name__)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost:5432/kahoot'

db.init_app(app)

# todo: use blueprint router
from usersRoutes import get_all_users, get_user_by_id, registration

@app.route('/')
def main():
    return 'Test koneksi dulu coy'
