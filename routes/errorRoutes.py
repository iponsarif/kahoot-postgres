from flask import jsonify, abort
from . import router

@router.errorhandler(403)
def error403(e):
    messages = {
        "status-code": 403,
        "message": "you belom login kayaknya, atau tokennya expired"
    }
    return jsonify(messages)

@router.errorhandler(404)
def error404(e):
    messages = {
        "status-code": 404,
        "message": "resource ga ketemu"
    }
    return jsonify(messages)

@router.errorhandler(500)
def error500(e):
    messages = {
        "status-code": 500,
        "message": "errorrrrrrr"
    }
    return jsonify(messages)    