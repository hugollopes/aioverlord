import logging
import os
import sys
import subprocess
import time
import re
from os import listdir
from os.path import isfile, join

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.info("launching e2e parallel tests")
os.system("rm reports/*.log")  # removing previous test files
os.system("mkdir kubernetese2e/applyfolder")

list_files = []
my_path = "./e2etests/features"
only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

for f in only_files:
    entry = dict()
    entry["feature"] = f
    entry["feature_namespace"] = "e2e-" + f.replace(".", "-").lower()
    list_files.append(entry)

test_number = 1

for f in list_files:
    os.system("rm kubernetese2e/applyfolder/*")  # removing previous templates
    os.system("cp -a kubernetese2e/orig/. kubernetese2e/applyfolder")
    os.system("rm kubernetese2e/applyfolder/e2etest-deployment.yaml")  # removing previous templates
    os.system("cp -a kubernetese2e/orignamespace/. kubernetese2e/applynamespace")
    os.system("sed -i -e 's/e2e-xxxx/" + f[
        "feature_namespace"] + "/' kubernetese2e/applynamespace/namespace.json")  # sednamespace
    os.system("kubectl apply -f kubernetese2e/applynamespace/namespace.json")
    os.system("kubectl config set-context minikube --namespace=" + f["feature_namespace"])

    os.system("kubectl delete -f kubernetese2e/applyfolder")
    os.system("kubectl apply -f kubernetese2e/applyfolder")

    os.system("cp kubernetese2e/orig/e2etest-deployment.yaml kubernetese2e/applyfolder")

    os.system(
        "sed -i -e 's/xxxx/" + f["feature"] + "/' kubernetese2e/applyfolder/e2etest-deployment.yaml")  # sed feature
    os.system("kubectl delete -f kubernetese2e/applyfolder/e2etest-deployment.yaml")
    time.sleep(5)
    os.system("kubectl apply -f kubernetese2e/applyfolder/e2etest-deployment.yaml")
    logging.info("launching test " + str(test_number) + " for feature: " + f["feature"])
    filepath = "./reports/e2eparallel" + str(test_number) + ".log"
    f["filepath"] = filepath
    logfile = open(filepath, "w+")
    f["file"] = logfile
    f["file"].close()
    test_number = test_number + 1

time.sleep(100)
for f in list_files:
    os.system("kubectl config set-context minikube --namespace=" + f["feature_namespace"])
    os.system("kubectl logs job/web >> " + f["filepath"])

logging.debug("merge log files")
logfile = open("reports/e2etest.log", "w+")
for f in list_files:
    logging.debug("merging filepath:" + f["filepath"])
    file = open(f["filepath"], "r")
    logfile.write("feature " + f["feature"] + " result in file:" + f["filepath"] + "\n")
    for line in file:
        if re.match("(.*)(scenario|step)(.*)", line):
            logfile.write(line)
    file.close()
logfile.close()
os.system("kubectl config set-context minikube --namespace=default")
print(open("reports/e2etest.log").read())
logging.info("E2E test ended")
