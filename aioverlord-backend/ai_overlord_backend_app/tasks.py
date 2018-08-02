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
    logging.debug("assign agent")
    if ('username' not in request_data) or ('agentId' not in request_data) or ('taskId' not in request_data):
        return jsonify({'error': "argumentsMissing"}), 400
    #agent = next(item for item in AGENTS if item["id"] == request_data["agentId"])
    #task = next(item for item in TASKS if item["id"] == request_data["taskId"])
    cursor = users.find_one({"username": request_data["username"]})
    if 'agents' not in dumps(cursor):
        return "user has no agent"
    if 'tasks' not in dumps(cursor):
        return "user has no task"
    agent_assigned = False
    for user_agent in cursor["agents"]:
        if user_agent["id"] == request_data["agentId"] and user_agent["status"] == "unassigned":
            for user_task in cursor["tasks"]:
                if user_task["id"] == request_data["taskId"] and user_task["status"] == "unassigned":
                    user_task["status"] = "assigned"
                    user_task["agentId"] = request_data["agentId"]
                    user_agent["status"] = "assigned"
                    agent_assigned = True
    if not agent_assigned:
        return "could not assign agent"
    mongo.db.users.save(cursor)
    return "agent assigned"


@available_tasks_route.route("/availableTasks", methods=['POST'])
@auth.login_required
@requires_roles('user')
def available_tasks_func():
    users = mongo.db.users
    request_data = request.get_json()
    logging.debug("available tasks")
    if 'username' not in request_data:
        return jsonify({'error': "argumentsMissing"}), 400
    cursor = users.find_one({"username": request_data["username"]})
    available_tasks = []
    if 'tasks' not in dumps(cursor):
        cursor["tasks"] = []
    for task in TASKS:
        user_has_task = False
        for user_task in cursor["tasks"]:
            if task["id"] == user_task["id"]:
                user_has_task = True
        if not user_has_task:
            task_copy = dict(task)
            task_copy["enabled"] = 'true'
            available_tasks.append(task_copy)
    return jsonify({'availableTasks': available_tasks})
