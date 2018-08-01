import logging
from ai_overlord_backend_app.globals import *
from ai_overlord_backend_app.database import mongo
from ai_overlord_backend_app.security import auth, requires_roles
from bson.json_util import dumps
from flask import Blueprint
from flask import request, jsonify

assign_agent_route = Blueprint('assign_agent_route', __name__)
available_tasks_route = Blueprint('available_tasks_route', __name__)


@assign_agent_route.route("/assignAgent", methods=['POST'])
@auth.login_required
@requires_roles('user')
def assign_agent():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("buy agent")
    if ('username' not in request_data) or ('agentId' not in request_data):
        return jsonify({'error': "argumentsMissing"}), 400
    agent = next(item for item in AGENTS if item["id"] == request_data["agentId"])
    cost = agent["cost"]
    cursor = users.find_one({"username": request_data["username"]})
    if int(cursor['credits']) < cost:
        logging.debug("not enough credits")
        return "not enough credits"
    if 'agents' not in dumps(cursor):
        cursor["agents"] = []
        cursor["agents"].append(agent)
    else:
        user_has_agent = False
        for user_agent in cursor["agents"]:
            if user_agent["id"] == user_agent["id"]:
                user_has_agent = True
        if not user_has_agent:
            cursor["agents"].append(agent)
        else:
            logging.debug("user already has agent")
            return "user already has agent"
    cursor["credits"] = cursor['credits'] - cost
    mongo.db.users.save(cursor)
    return "agent purchased"


@available_tasks_route.route("/availableTasks", methods=['POST'])
@auth.login_required
@requires_roles('user')
def available_agent_func():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("available agents")
    if 'username' not in request_data:
        return jsonify({'error': "argumentsMissing"}), 400
    cursor = users.find_one({"username": request_data["username"]})
    available_agents = []
    user_credits = cursor["credits"]
    if 'agents' not in dumps(cursor):
        cursor["agents"] = []
    for agent in AGENTS:
        user_has_agent = False
        for user_agent in cursor["agents"]:
            if agent["id"] == user_agent["id"]:
                user_has_agent = True
        if not user_has_agent:
            agent_copy = dict(agent)
            agent_copy["enabled"] = 'true' if user_credits >= agent["cost"] else 'false'
            available_agents.append(agent_copy)
    return jsonify({'availableAgents': available_agents})