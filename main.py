from flask import Flask, request
import os
import datetime
from flask import jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
import platform
import gridfs
import json


cwd = os.getcwd()

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


@app.route("/create_classification")
def new_classification():
    result = mongo.db.classification.insert_one(
        {
            "name": "is_triangle",
            "labels": [ "yes", "no"]
        }
    )
    return str(result)


@app.route("/getuser")
def get_user():
    users = mongo.db.users
    cursor = users.find_one({"name": "testUser1"})
    #calculate seconds between now and database.
    timestamp_db = int(cursor['timestamp'])
    timestamp = int(datetime.datetime.now().timestamp())
    #calculate saved ticks
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


@app.route("/savepicturetests")
def savepicturetests():
    image_dir = os.path.join(cwd,"static","images")
    image_path = os.path.join(image_dir,"neural.jpg")
    pictures = mongo.db.pictures
    image = open(image_path, "rb")
    fs = gridfs.GridFS(mongo.db)
    fs_id = fs.put(image.read(), filename="neural.jpg")
    data = {"about": "neural.jpg", "file_id": fs_id}
    pictures.insert(data)
    return image_dir

@app.route("/retrievepictests")
def retrievepictests():
    image_dir = os.path.join(cwd, "static", "images","unclassified")
    image_path = os.path.join(image_dir, "image.jpg")
    fs = gridfs.GridFS(mongo.db)
    image_file = fs.get_last_version("image.jpg")
    file = open(image_path, 'wb')
    file.write(image_file.read())
    file.close()
    return "done"


@app.route("/classify")
def classify():
    api_return = {
        "name": "is_triangle",
        "labels": [ "yes", "no"],
        "images": ["./images/unclassified/image.jpg","./images/unclassified/neural.jpg"]
        }
    return json.dumps(api_return)


@app.route("/saveclassification", methods=['POST'])
def save_classification():
    request_data = request.get_json()
    pictures = mongo.db.pictures
    datetime_string = datetime.datetime.now().timestamp()
    cursor = pictures.update(
        {"file_id": request_data["file_id"]},
        {
            "file_id": request_data["file_id"],
            "labeled": request_data["labeled"],
            "timestamp": datetime_string
        },
        upsert=True
    )
    return dumps(cursor)


#todo: does not work in ubunto
@app.route('/')
@app.route('/<path:path>')
def root(path):
    print(path)
    return app.send_static_file(path)

#needed to allow API access from any site.
@app.after_request
def after_request(response):
  response.headers.add('Access-Control-Allow-Origin', '*')
  response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
  response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
  return response


if __name__ == "__main__":
    # Check the System Type before to decide to bind
    # If the system is a Linux machine -:)
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True)
    # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='127.0.0.1', port=50000, debug=True)
