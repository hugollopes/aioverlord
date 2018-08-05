import os
import shlex
import logging
import subprocess
import requests
from time import sleep
import sys

#misses the changing of the IP of flask... flask must be deployed before.
#misses the copy here before the build
#os.system("docker build  ./nginx/  --tag localhost:5001/nginx:latest")
#os.system("docker push localhost:5001/nginx:latest")


url = "http://10.97.89.39:5000/createUser"
print("url:" + url)
data = '{  "username": "admin@aioverlord.com",  "password": "admin",  "role": "admin"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response admin user creation: " + str(response))
data = '{  "username": "user@aioverlord.com",  "password": "hackme",  "role": "user"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response normal user creation: " + str(response))