import os
import json
#from bson.json_util import dumps
from flask import request, jsonify

clusterflaskIP = os.popen("kubectl get services/flask --namespace=prod -o go-template='{{(index .spec.clusterIP)}}'").read()
print("flaskserver :" + clusterflaskIP)



jason_file =open("./referenceData/prodIPs.json", encoding='utf-8')
data = json.loads(jason_file.read())
jason_file.close()


data["prodflaskDNS"] = clusterflaskIP
print(data)
jason_file = open("./referenceData/prodIPs.json", "w+")
jason_file.write(json.dumps(data))
jason_file.close()
