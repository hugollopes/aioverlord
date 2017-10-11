from flask import Blueprint
import datetime

from bson.json_util import dumps
from flask import Blueprint
from flask import request

from ai_overlord_backend_app.database import mongo

# blueprint definition
get_user_route = Blueprint('get_user_route', __name__)
save_user_route = Blueprint('save_user_route', __name__)
create_user_route = Blueprint('create_user_route', __name__)


@get_user_route.route("/getuser")
def get_user():
    users = mongo.db.users
    cursor = users.find_one({"name": "testUser1"})
    # calculate seconds between now and database.
    timestamp_db = int(cursor['timestamp'])
    timestamp = int(datetime.datetime.now().timestamp())
    # calculate saved ticks
    # for x in range(timestamp - timestamp_db):
    #    cursor['cash'] = cursor['cash'] + 1 + cursor['factory1Level'] * 1 + cursor['factory2Level'] * 10;
    #    print('cursor cash:',cursor['cash'])
    cursor['cash'] = (cursor['cash'] + 1 + cursor['factory1Level'] * 1 +
                      cursor['factory2Level'] * 10)*(timestamp - timestamp_db)
    return dumps(cursor)


# todo validate post request
@save_user_route.route("/saveuser", methods=['POST'])
def save_user():
    request_data = request.get_json()
    users = mongo.db.users
    datetime_string = datetime.datetime.now().timestamp()
    cursor = users.update(
        {"name": request_data["name"]},
        {
            "name": request_data["name"],
            "cash": request_data["cash"],
            "factory1Level": request_data["factory1Level"],
            "factory2Level": request_data["factory2Level"],
            "timestamp": datetime_string
        },
        upsert=True
    )
    return dumps(cursor)


@create_user_route.route("/createuser")
def new_user():
    result = mongo.db.users.insert_one(
        {
            "name": "testUser1",
            "cash": 10,
            "factory1Level": 1,
            "factory2Level": 2,
            "timestamp": datetime.datetime.now().timestamp()
        }
    )
    return result
