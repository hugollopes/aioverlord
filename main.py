from flask import Flask, request
import datetime
from flask import jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
import platform

app = Flask(__name__, static_url_path='')

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/local'

mongo = PyMongo(app)


@app.route("/createuser")
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


@app.route("/getuser")
def get_user():
    users = mongo.db.users
    cursor = users.find_one({"name": "testUser1"})
    #calculate seconds between now and database.
    timestamp_db = int(cursor['timestamp'])
    timestamp = int(datetime.datetime.now().timestamp())
    for x in range(timestamp - timestamp_db):
        cursor['cash'] = cursor['cash'] + 1 + cursor['factory1Level'] * 1 + cursor['factory2Level'] * 10;
        print('cursor cash:',cursor['cash'])
    return dumps(cursor)


# todo validate post request
@app.route("/saveuser", methods=['POST'])
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


@app.route("/")
def hello():
    return "alive"


@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)


if __name__ == "__main__":
    # Check the System Type before to decide to bind
    # If the system is a Linux machine -:)
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True)
    # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='127.0.0.1', port=50000, debug=True)
