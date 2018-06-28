import logging
import os
import sys
import subprocess
import time
import re
from os import listdir
from os.path import isfile, join


os.system("kubectl delete namespaces e2e-e2e-test-feature")
os.system("kubectl delete namespaces e2e-topology-feature")
os.system("kubectl delete namespaces e2e-labeldata-feature")
os.system("kubectl delete namespaces e2e-debugfunctions-feature")
os.system("kubectl delete namespaces e2e-mainpage-feature")
os.system("kubectl delete namespaces e2e-user-feature")
os.system("kubectl config set-context minikube --namespace=default")
os.system("kubectl delete -f ./kubernetes")

