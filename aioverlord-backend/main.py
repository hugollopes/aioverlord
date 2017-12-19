import os
import platform
import sys
import logging
from io import BytesIO
from ai_overlord_backend_app.classification import *
from ai_overlord_backend_app.user import *
from flask import Flask
from flask_httpauth import HTTPBasicAuth





logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)
cwd = os.getcwd()

app = Flask(__name__, static_url_path='')
# configure DB
app.config['MONGO_DBNAME'] = 'restdb'
app.config['MONGO_URI'] = 'mongodb://db:27017/local'

# blueprints
app.register_blueprint(classify_route)
app.register_blueprint(create_classification_route)
app.register_blueprint(save_classification_route)
app.register_blueprint(get_user_route)
app.register_blueprint(update_user_route)
app.register_blueprint(create_user_route)
app.register_blueprint(get_token_route)

auth = HTTPBasicAuth()



mongo.init_app(app)


# debugging message
@app.route('/')
def dummy_root():
    logging.debug("server alive2")
    user = mongo.db.users
    timestamp = int(datetime.datetime.now().timestamp())
    user.insert({
            "username": "test",
            "email": "user"
        })
    return "server alive2"


@app.route('/uploadpicture', methods=['POST'])
def upload_picture():
    request_data = request.get_json()
    print("request_data: " + request_data["file_data"])
    image = BytesIO(base64.b64decode(request_data["file_data"]))
    fs = gridfs.GridFS(mongo.db)
    fs_id = fs.put(image.read(), filename=request_data["file_name"])
    data = {"file_name": request_data["file_name"], "file_id": fs_id}
    pictures = mongo.db.pictures
    pictures.insert(data)
    return "inserted"


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
def retrieve_pic_tests():
    image_dir = os.path.join(cwd, "static", "images","unclassified")
    image_path = os.path.join(image_dir, "neural3.jpg")
    fs = gridfs.GridFS(mongo.db)
    image_file = fs.get_last_version("neural3.jpg")
    file = open(image_path, 'wb')
    file.write(image_file.read())
    file.close()
    return "done"


@app.route('/<path:path>')
def root(path):
    print(path)
    return app.send_static_file(path)


# needed to allow API access from any site.
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
        # app.run(host='0.0.0.0', port=5000, debug=True, ssl_context=('cert.pem', 'key.pem'))
    # If the system is a windows /!\ Change  /!\ the   /!\ Port
    elif platform.system() == "Windows":
        app.run(host='127.0.0.1', port=50000, debug=True)
