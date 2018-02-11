import datetime
import logging
from ai_overlord_backend_app.globals import *
from ai_overlord_backend_app.database import mongo
from ai_overlord_backend_app.security import auth, generate_auth_token, token_expire, requires_roles
from bson.json_util import dumps
from flask import Blueprint, g
from flask import request, jsonify, abort
from passlib.apps import custom_app_context as pwd_context

buy_topology_route = Blueprint('buyTopology', __name__)


@buy_topology_route.route("/buyTopology", methods=['POST'])
@auth.login_required
@requires_roles('user')
def buy_topology():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("buy topology")
    if ('username' not in request_data) or ('topologyId' not in request_data):
        return jsonify({'error': "argumentsMissing"}), 400
    topology = next(item for item in TOPOLOGIES if item["id"] == request_data["topologyId"])
    cost = topology["cost"]
    cursor = users.find_one({"username": request_data["username"]})
    if int(cursor['credits']) < cost:
        logging.debug("not enough credits")
        return "not enough credits"
    cursor["credits"] = cursor['credits'] - cost
    if 'topologies' not in dumps(cursor):
        cursor["topologies"] = []
        cursor["topologies"].append(topology)
    else:
        cursor["topologies"].append(topology)
    mongo.db.users.save(cursor)
    return "topology purchased"


@buy_topology_route.route("/availableTopologies", methods=['POST'])
@auth.login_required
@requires_roles('user')
def available_topologies_func():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("available topologies")
    if 'username' not in request_data:
        return jsonify({'error': "argumentsMissing"}), 400
    cursor = users.find_one({"username": request_data["username"]})
    available_topologies = []
    for topology in TOPOLOGIES:
        user_has_topology = False
        for user_topology in cursor["topologies"]:
            if topology["id"] == user_topology:
                user_has_topology = True
        if not user_has_topology:
            available_topologies.append(topology)
    return dumps(available_topologies)
