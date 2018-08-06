import os
import sys
import shlex
import logging
import subprocess
import requests
from time import sleep







logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.info("populating dev enviroment")

# apply
#os.system("kubectl apply -f kubernetes/devnamespace.json")
#os.system("kubectl apply -f kubernetes/kubernetesdev")

# seed data
sleep(10)  # wait for 10 second
ip_port = os.popen('echo "'+"$(kubectl get ep/flask -o jsonpath='{.subsets[0].addresses[0].ip}'):$(kubectl get ep/flask -o jsonpath='{.subsets[0].ports[0].port}')" + '"').read().rstrip()
# url = 'http://' + ip_port + '/createUser'
url = "http://localhost:8001/api/v1/namespaces/dev/services/flask/proxy/createUser"
print("url:" + url)
data = '{  "username": "admin@aioverlord.com",  "password": "admin",  "role": "admin"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response admin user creation: " + str(response))
data = '{  "username": "user@aioverlord.com",  "password": "hackme",  "role": "user"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response normal user creation: " + str(response))
# web_url =os.popen('echo "'+ "$(kubectl get ep/web -o jsonpath='{.subsets[0].addresses[0].ip}'):$(kubectl get ep/web -o jsonpath='{.subsets[0].ports[0].port}')" + '"').read()
os.system("chromium-browser 'http://localhost:8001/api/v1/namespaces/dev/services/web/proxy/#/'")
logging.info("finishing launching dev environment")
