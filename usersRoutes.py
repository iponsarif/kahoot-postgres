from flask import request, json, jsonify, make_response
from datetime import datetime, timezone

from utils import utc7, generateToken
from app import app
from models import db, Users

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
    response = {}
    body = request.json

    username = body['username']
    password = body['password']
    fullname = body['fullname']
    email = body['email']
    
    try:
        user = Users(
            username = username,
            password = password,
            fullname = fullname,
            email = email,
            )
        db.session.add(user)
        db.session.commit()
        # return 'Registration successful. user id ={}'.format(user.id)
        response['message'] = 'Registration success, please login!'
        statusCode = 200
    except Exception as e:
        response['message'] = 'Registration failed'
        response['Error'] = str(e)
        statusCode = 400
    
    return jsonify(response), statusCode

# login + generate token
@app.route('/login', methods=['POST'])
def login():
    response = {}
    body = request.json
    print(body)
    username = body['username']
    password = body['password']
    isLogin = False

    try:
        users = get_all_users().json
        for user in users:
            if username == user['username']:
                if password == user['password']:
                    isLogin = True
                    
    except Exception as e:
        response['Error'] = str(e)
        # return str(e)
    
    if isLogin:
        response['message'] = 'Login success, welcome {}'.format(username)
        response['token'] = generateToken(username)
        statusCode = 200
        
    else:
        response['message'] = 'Login failed, username or password is wrong'
        statusCode = 400

    finalResponse = make_response(jsonify(response), statusCode)
    finalResponse.set_cookie('username', value=username)

    print('finalssss',finalResponse)
    return finalResponse

# cookies
# def set_cookies(username):
#     resp = make_response('')
#     resp.set_cookie('username', username)
#     return resp

# update user by user.id
@app.route('/updateUser/<id_>', methods=['POST'])
def update_user(id_):
    # ngambil dulu data user yang mau diupdate, antisipasi kalo tidak semua kolom diupdate
    user = get_user_by_id(id_).json 
    print(user)
    body = request.json    
    # modified_at = utc7(datetime.utcnow())
    
    # print(modified_at)
    # kalau yg diupdate tidak semua kolom
    if 'username' not in body:
        username = user['username']
    else:
        username = body['username']

    if 'password' not in body:
        password = user['password']
    else:
        password = body['password']

    if body['fullname']:
    # if 'fullname' not in body:
        fullname = user['fullname']
    else:
        fullname = body['fullname']
        
    if 'email' not in body:
        email = user['email']        
    else:
        email = body['email']
        
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