import logging
from functools import wraps

from ai_overlord_backend_app.database import mongo
from flask import g, jsonify, request
from flask_httpauth import HTTPBasicAuth
from itsdangerous import (TimedJSONWebSignatureSerializer
                          as Serializer, BadSignature, SignatureExpired)
from passlib.apps import custom_app_context as pwd_context

auth = HTTPBasicAuth()
token_expire = 50000

secret_key = "this needs to change and not be in the code like this"  # todo: must be dependant of some outside conf.


def generate_auth_token(user_id, expiration=50000):
    s = Serializer(secret_key, expires_in=expiration)
    token = s.dumps({'id': user_id})
    logging.debug("token created")
    return token


def verify_auth_token(token):
    s = Serializer(secret_key)
    try:
        data = s.loads(token)
    except SignatureExpired:
        return None  # valid token, but expired
    except BadSignature:
        return None  # invalid token
    return data['id']


def get_current_user_role():
    return g.role


def error_response():
    return jsonify({'error': "userHasNoAuthorization"}), 400


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if get_current_user_role() not in roles:
                return error_response()
            return f(*args, **kwargs)

        return wrapped

    return wrapper


@auth.verify_password
def verify_password(username, password):  # don't work.  get variables from request
    user = mongo.db.users.find_one({"username": request.json.get('username')})
    g.current_user_id = str(user['_id'])
    g.role = str(user['role'])
    if not user:
        logging.debug("authentication user does not exist: " + str(request.json.get('username')))
        return False
    user_id = ''
    if request.json.get('token') is not None:
        user_id = verify_auth_token(request.json.get('token'))
        # logging.debug("user_id : " + str(user_id)  + "request.json.get('token'): "
        # + request.json.get('token') + "user['_id'] : " + str(user['_id']))
    if str(user_id) != str(user['_id']):
        logging.debug("token auth failed: " + str(request.json.get('token')))
        if not pwd_context.verify(str(request.json.get('password')), str(user['password'])):
            logging.debug("authentication user password is wrong: " + str(request.json.get('password')))
            return False
    logging.debug("authentication successful: " + request.json.get('username'))
    return True
