from flask import request, g
from functools import wraps

from .crypt import encrypt, decrypt
from .token import encode, decode

import jwt

def generateToken(data):
    data = encrypt(data)
    token = encode(data)
    
    return token

def verifyLogin(f):
    @wraps(f)
    def decoratedFunction(*args, **kwargs):
        token = request.headers["Authorization"][7:]

        data = decode(token)
        username = decrypt(data["data"])
        g.username = username

        return f(*args, **kwargs)
    return decoratedFunction