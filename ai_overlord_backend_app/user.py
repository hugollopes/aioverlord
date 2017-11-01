import datetime
import logging

from bson.json_util import dumps
from flask import Blueprint, g
from flask import request, jsonify, abort
from passlib.apps import custom_app_context as pwd_context
from ai_overlord_backend_app.database import mongo
from ai_overlord_backend_app.security import auth, generate_auth_token, verify_auth_token, token_expire


# blueprint definition
get_user_route = Blueprint('get_user_route', __name__)
update_user_route = Blueprint('update_user_route', __name__)
create_user_route = Blueprint('create_user_route', __name__)
get_token_route = Blueprint('get_token_route', __name__)


@auth.verify_password
def verify_password(username, password):  # don't work.  get variables from request
    user = mongo.db.users.find_one({"username": request.json.get('username')})
    g.current_user_id = str(user['_id'])
    if not user:
        logging.debug("authentication user does not exist: " + str(request.json.get('username')))
        return False
    user_id = ''
    if request.json.get('token') is not None:
        user_id = verify_auth_token(request.json.get('token'))
        logging.debug("user_id : " + str(user_id)  + "request.json.get('token'): " + request.json.get('token') + "user['_id'] : " + str(user['_id']))
    if str(user_id) != str(user['_id']):
        logging.debug("token auth failed: " + str(request.json.get('token')))
        if not pwd_context.verify(str(request.json.get('password')), str(user['password'])):
            logging.debug("authentication user password is wrong: " + str(request.json.get('password')))
            return False
    logging.debug("authentication successful: " + request.json.get('username'))
    return True


@create_user_route.route("/createUser", methods=['POST'])
def create_user():
    username = request.json.get('username')
    password = request.json.get('password')
    user = mongo.db.users
    if username is None or password is None:
        return jsonify({'error': "argumentsMissing"}), 400
    if user.find_one({"username": username}) is not None:
        return jsonify({'error': "userAlreadyExists"}), 400
    timestamp = int(datetime.datetime.now().timestamp())
    user.insert({
            "username": username,
            "email": username,
            "password": pwd_context.encrypt(password),
            "credits": 10,
            "neurons": 1,
            "timestamp": timestamp
        })
    return jsonify({'username': username}), 201


@get_user_route.route("/getuser", methods=['POST'])
@auth.login_required
def get_user():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("request dump" + dumps(request_data))
    cursor = users.find_one({"username": request_data["username"]})
    # calculate seconds between now and database.
    timestamp_db = int(cursor['timestamp'])
    timestamp = int(datetime.datetime.now().timestamp())
    # calculate saved ticks
    for x in range(timestamp - timestamp_db):
        cursor['credits'] = cursor['credits'] + 1 + cursor['neurons'] * 1
    logging.debug("ticks: " + str(range(timestamp - timestamp_db)))
    cursor["timestamp"] = datetime.datetime.now().timestamp()
    mongo.db.users.save(cursor)
    logging.debug("update_cursor: " + dumps(cursor))
    return dumps(cursor)


@update_user_route.route("/updateUserStatus", methods=['POST'])
def update_user_status():
    request_data = request.get_json()
    if request_data["username"] is None or request_data["password"] is None \
       or request_data["credits"] is None or request_data["neurons"] is None:
        abort(400)  # missing arguments
    user = mongo.db.users.find_one({"username": request_data["username"]})
    if user is None:
        return jsonify({'error': "user does not exist"}), 400
    user["credits"] = request_data["credits"]
    user["neurons"] = request_data["neurons"]
    user["timestamp"] = datetime.datetime.now().timestamp()
    mongo.db.users.save(user)
    return jsonify({'status': 'user updated'}), 200


@get_token_route.route("/gettoken", methods=['POST'])
@auth.login_required
def update_user_status():
    logging.debug("request dump" + dumps(request.get_json()))
    token = generate_auth_token(g.current_user_id, token_expire).decode('ascii')
    logging.debug("token: " + token)
    return jsonify({'token': token}), 200



