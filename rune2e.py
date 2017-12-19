import logging
import os, sys
from os import listdir
from os.path import isfile, join

logging.basicConfig(stream=sys.stderr, level=logging.INFO)
logging.info("launching e2e parallel tests")

my_path = "./aioverlord-frontend/features"
only_files = [f for f in listdir(my_path) if isfile(join(my_path, f))]

test_number = 1
os.environ["FEATURECOMMAND"] = "--"
for f in only_files:
    logging.info("launching test " + str(test_number) + "for feature: " + f)
    os.environ["TESTFEATURE"] = "features/" + f
    os.system("docker-compose -f e2e-test.yml -p test" + str(test_number) + " up -d")
    test_number = test_number + 1

os.environ["FEATURECOMMAND"] = ""
os.environ["TESTFEATURE"] = "--"
logging.info("E2E test ended")
