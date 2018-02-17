import logging
from ai_overlord_backend_app.globals import *
from ai_overlord_backend_app.database import mongo
from ai_overlord_backend_app.security import auth, requires_roles
from bson.json_util import dumps
from flask import Blueprint
from flask import request, jsonify

buy_topology_route = Blueprint('buy_topology_route', __name__)
available_topologies_route = Blueprint('available_topologies_route', __name__)


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
    if 'topologies' not in dumps(cursor):
        cursor["topologies"] = []
        cursor["topologies"].append(topology)
    else:
        user_has_topology = False
        for user_topology in cursor["topologies"]:
            if topology["id"] == user_topology["id"]:
                user_has_topology = True
        if not user_has_topology:
            cursor["topologies"].append(topology)
        else:
            logging.debug("user already has topology")
            return "user already has topology"
    cursor["credits"] = cursor['credits'] - cost
    mongo.db.users.save(cursor)
    return "topology purchased"


@available_topologies_route.route("/availableTopologies", methods=['POST'])
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
    user_credits = cursor["credits"]
    if 'topologies' not in dumps(cursor):
        cursor["topologies"] = []
    for topology in TOPOLOGIES:
        user_has_topology = False
        for user_topology in cursor["topologies"]:
            if topology["id"] == user_topology["id"]:
                user_has_topology = True
        if not user_has_topology:
            topology_copy = dict(topology)
            topology_copy["enabled"] = 'true' if user_credits >= topology["cost"] else 'false'
            available_topologies.append(topology_copy)
    return jsonify({'availableTopologies': available_topologies})
