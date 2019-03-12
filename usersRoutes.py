from flask import request, json, jsonify
from datetime import datetime, timezone

from utils import utc7
from models import Users
from app import app
from models import db

# get All Users
@app.route('/getAllUsers', methods=['GET'])
def get_all_users():
    try:
        users = Users.query.order_by(Users.id).all()
        return jsonify([usr.serialize() for usr in users])
    except Exception as e:
        return(str(e))

# get user by id
@app.route('/getUser/<id_>', methods=['GET'])
def get_user_by_id(id_):
    try:
        user = Users.query.filter_by(id=id_).first()
        return jsonify(user.serialize())
    except Exception as e:
        return(str(e))

# registration
@app.route('/registration', methods=['POST'])
def registration():
    username = request.args.get('username')
    password = request.args.get('password')
    fullname = request.args.get('fullname')
    email = request.args.get('email')
    
    try:
        user = Users(
            username = username,
            password = password,
            fullname = fullname,
            email = email,
            )
        db.session.add(user)
        db.session.commit()
        return 'Registration successful. user id ={}'.format(user.id)
    except Exception as e:
        return(str(e))

# update user by user.id
@app.route('/updateUser/<id_>', methods=['POST'])
def update_user(id_):
    # ngambil dulu data user yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    user = get_user_by_id(id_).json 
    
    username = request.args.get('username')
    password = request.args.get('password')
    fullname = request.args.get('fullname')
    email = request.args.get('email')
    # modified_at = utc7(datetime.utcnow())
    
    # print(modified_at)
    # kalau yg diupdate tidak semua kolom
    if username is None:
        username = user['username']

    if password is None:
        password = user['password']

    if fullname is None:
        fullname = user['fullname']
        
    if email is None:
        email = user['email']        
           
    try:
        user_ = {
            'username': username,
            'password': password,
            'fullname': fullname,
            'email': email,
            # 'modified_at': modified_at
        }
        
        db.session.query(Users).filter(Users.id==id_).update(user_)
        db.session.commit()
        return 'User updated. user id ={}'.format(id_)
    except Exception as e:
        return(str(e))

# hard delete user by id
@app.route('/deleteUser/<id_>', methods=['DELETE'])
def delete_user(id_):
    try:
        user = Users.query.filter_by(id=id_).first()
        db.session.delete(user)
        db.session.commit()
        return 'User deleted. user id={}'.format(id_)
    except Exception as e:
        return(str(e))