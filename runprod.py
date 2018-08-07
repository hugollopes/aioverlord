import os
import shlex
import logging
import subprocess
import requests
from time import sleep
import sys

sleep(5)
clusterflaskIP = os.popen("kubectl get services/flask --namespace=prod -o go-template='{{(index .spec.clusterIP)}}'").read()
clusterwebIP = os.popen("kubectl get services/web --namespace=prod -o go-template='{{(index .spec.clusterIP)}}'").read()
url = "http://" +clusterflaskIP +":5000/createUser"
print("url:" + url)
data = '{  "username": "admin@aioverlord.com",  "password": "admin",  "role": "admin"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response admin user creation: " + str(response))
data = '{  "username": "user@aioverlord.com",  "password": "hackme",  "role": "user"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response normal user creation: " + str(response))

os.system("chromium-browser 'http://" +clusterwebIP +"/static/index.html'")


