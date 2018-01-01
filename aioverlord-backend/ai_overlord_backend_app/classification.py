import base64
import datetime
import logging

import gridfs
from ai_overlord_backend_app.database import mongo
from ai_overlord_backend_app.security import auth, requires_roles
from bson.json_util import dumps
from bson.objectid import ObjectId
from flask import Blueprint
from flask import request

# blueprint definition
classify_route = Blueprint('classify_route', __name__)
create_classification_route = Blueprint('create_classification_route', __name__)
save_classification_route = Blueprint('save_classification_route', __name__)


@classify_route.route("/classify", methods=['POST'])
@auth.login_required
@requires_roles('user')
def classify():
    # get classification
    # todo: randomize classification or set it as input
    classification_collection = mongo.db.classification
    classification_cursor = classification_collection.find_one({"name": "is_triangle"})

    logging.debug("classification_cursor: " + dumps(classification_cursor))

    # todo: evolve picture label systems, randomize selection
    # get picture with the classification not set
    picture_collection = mongo.db.pictures
    picture_cursor = picture_collection.find_one({"labeled": None})
    logging.debug("picture_cursor: " + dumps(picture_cursor))
    if picture_cursor is not None:
        # get picture base64 string
        fs = gridfs.GridFS(mongo.db)
        picture_file = fs.get(picture_cursor["file_id"])

        logging.debug("picture_file_cursor:  " + dumps(picture_file))

        # buildup json
        api_return = {
            "name": classification_cursor["name"],
            "labels": classification_cursor["labels"],
            "image_name": picture_cursor["file_name"],
            "file_id": str(picture_cursor["file_id"]),
            "image": base64.standard_b64encode(picture_file.read()).decode("ascii")
        }
        return dumps(api_return)
    else:
        return "no results"


@create_classification_route.route("/create_classification", methods=['POST'])
def new_classification():
    result = mongo.db.classification.insert_one(
        {
            "name": "is_triangle",
            "labels": ["yes", "no"]
        }
    )
    return str(result)


# todo:misses validation and authentication
@save_classification_route.route("/saveclassification", methods=['POST'])
@auth.login_required
@requires_roles('user')
def save_classification():
    request_data = request.get_json()
    logging.debug("request_data: " + dumps(request_data))
    pictures = mongo.db.pictures
    datetime_string = datetime.datetime.now().timestamp()
    cursor = pictures.update(
        {"file_id": ObjectId(request_data["file_id"])}, {
            "$set": {
                "file_id": ObjectId(request_data["file_id"]),
                "labeled": request_data["labeled"],
                "timestamp": datetime_string
            }
        }
    )
    logging.debug("update result: " + dumps(cursor))
    return dumps(cursor)
