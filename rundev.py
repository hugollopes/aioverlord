import os
import sys
import shlex
import logging
import subprocess
import requests
from time import sleep


logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.info("launching dev environment")
os.system("docker-compose -f dev.yml -p dev build")
p = subprocess.Popen(shlex.split("docker-compose -f dev.yml -p dev up  --force-recreate --build"))
sleep(10)  # wait for 10 second
url = 'http://localhost:5000/createUser'
data = '{  "username": "admin@aioverlord.com",  "password": "admin",  "role": "admin"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})

logging.info("response admin user creation: " + str(response))
url = 'http://localhost:5000/createUser'
data = '{  "username": "user@aioverlord.com",  "password": "hackme",  "role": "user"}'
response = requests.post(url, data=data, headers={"Content-Type": "application/json"})
logging.info("response normal user creation: " + str(response))
os.system("chromium-browser 'http://localhost:8080/#/'")
logging.info("finishing launching dev environment")
