import os
import sys
import shlex
import logging
import subprocess
import requests
from time import sleep

os.system("kubectl config set-context minikube --namespace=default")
# stop sessions

os.system("kubectl config set-context minikube --namespace=default")
os.system("kubectl delete -f ./kubernetes/web-deployment.yaml")
os.system("kubectl delete -f ./kubernetes/flask-deployment.yaml")
os.system("kubectl delete -f ./kubernetes/mongodb-deployment.yaml")


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.info("launching dev environment")
# building
os.system("docker build  ./aioverlord-frontend/  --tag localhost:5001/frontend:latest")
os.system("docker build  ./aioverlord-backend/  --tag localhost:5001/backend:latest")
os.system("docker build  ./e2etests/  --tag localhost:5001/e2etest:latest")
os.system("docker build  ./aliveprobe/  --tag localhost:5001/aliveprobe:latest")

# pushing
os.system("docker push localhost:5001/frontend:latest")
os.system("docker push localhost:5001/mongo:3.5")
os.system("docker push localhost:5001/backend:latest")
os.system("docker push localhost:5001/e2etest:latest")
os.system("docker push localhost:5001/aliveprobe:latest")

# log command: kubectl logs -f deployment/flask      

# apply
p = subprocess.Popen(shlex.split("kubectl apply -f kubernetes/kubernetesdev"))

# seed data
sleep(10)  # wait for 10 second
ip_port = os.popen('echo "'+"$(kubectl get ep/flask -o jsonpath='{.subsets[0].addresses[0].ip}'):$(kubectl get ep/flask -o jsonpath='{.subsets[0].ports[0].port}')" + '"').read().rstrip()
# url = 'http://' + ip_port + '/createUser'
url = "http://localhost:8001/api/v1/namespaces/default/services/flask/proxy/createUser"
print("url:" + url)
data = '{  "username": "admin@aioverlord.com",  "password": "admin",  "role": "admin"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response admin user creation: " + str(response))
data = '{  "username": "user@aioverlord.com",  "password": "hackme",  "role": "user"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response normal user creation: " + str(response))
# web_url =os.popen('echo "'+ "$(kubectl get ep/web -o jsonpath='{.subsets[0].addresses[0].ip}'):$(kubectl get ep/web -o jsonpath='{.subsets[0].ports[0].port}')" + '"').read()
os.system("chromium-browser 'http://localhost:8001/api/v1/namespaces/default/services/web/proxy/#/'")
logging.info("finishing launching dev environment")
