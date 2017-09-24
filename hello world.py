from flask import Flask
from flask import Response
from flask import jsonify

app = Flask(__name__, static_url_path='')



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

@app.route("/")
def hello():
    user = make_user("hugo",14)
    resp = jsonify(
        name=user.name,
        age=user.age,
        )
    #resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp

@app.route("/attack")
def hellow():
    return "Hello World!2222"

@app.route('/<path:path>')
def root(path):
    return app.send_static_file(path)
    #return "here"

if __name__ == "__main__":
    app.run()




