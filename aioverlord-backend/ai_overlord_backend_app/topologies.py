import datetime
import logging

from ai_overlord_backend_app.database import mongo
from ai_overlord_backend_app.security import auth, generate_auth_token, token_expire, requires_roles
from bson.json_util import dumps
from flask import Blueprint, g
from flask import request, jsonify, abort
from passlib.apps import custom_app_context as pwd_context

buy_topology_route = Blueprint('buyTopology', __name__)

topologies = [{"id": 1, "name": "2 hidden layers", "cost": 10},
              {"id": 2, "name": "3 hidden layers", "cost": 100}]


@buy_topology_route.route("/buyTopology", methods=['POST'])
@auth.login_required
@requires_roles('user')
def buy_neuron():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("buy topology")
    if ('username' not in request_data) or ('topologyId' not in request_data):
        return jsonify({'error': "argumentsMissing"}), 400
    topology = next(item for item in topologies if item["id"] == 1)["cost"]
    cost = topology["cost"]
    cursor = users.find_one({"username": request_data["username"]})
    if int(cursor['credits']) < cost:
        logging.debug("not enough credits")
        return "not enough credits"
    cursor["credits"] = cursor['credits'] - cost
    cursor["topologies"] = cursor["topologies"].append(topology)
    mongo.db.users.save(cursor)
    return "topology purchased"
