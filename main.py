from flask import Flask
from flask import Response
from flask import jsonify
from flask_pymongo import PyMongo
from bson.json_util import dumps
import platform

app = Flask(__name__, static_url_path='')

app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://localhost:27017/local'

mongo = PyMongo(app)


class User(object):
    name = ""
    age = 0

    # The class "constructor" - It's actually an initializer
    def __init__(self, name, age, ):
        self.name = name
        self.age = age


def make_user(name, age):
    student = User(name, age, )
    return student

@app.route("/createuser")
def new_user():
    result = mongo.db.users.insert_one(
        {
            "name": "testUser1",
            "cash": 10,
            "factory1Level": 1,
            "factory2Level": 2
            }
    )
    return "done"


@app.route("/getuser")
def get_user():
    users = mongo.db.users
    cursor = users.find_one({"name": "testUser1"})
    return dumps(cursor)



@app.route("/")
def hello():
    user = make_user("hugo",14)
    resp = jsonify(
        name=user.name,
        age=user.age,
        )
    #resp.headers['Access-Control-Allow-Origin'] = '*'sdsdfffsdf
    return resp

@app.route("/attack")
def hellow():
    star = mongo.db.users
    output = []
    for s in star.find():
        output.append({'name': s['name'], 'id': s['id']})
    return jsonify({'result': output})
    #return "Hello World!2222"

@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)
    #return "here"

if __name__ == "__main__":
    # Check the System Type before to decide to bindd
    # If the system is a Linux machine -:)
    if platform.system() == "Linux":
        app.run(host='0.0.0.0', port=5000, debug=True)
    # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='127.0.0.1', port=50000, debug=True)





