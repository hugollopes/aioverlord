#!/usr/bin/env bash
#docker build
docker-compose -f dev.yml build
docker-compose -f dev.yml up



docker run -it -v "$(pwd)":/app web bash

docker run -it --mount type=bind,source="$(pwd)"/.,target=/app web bash

#from inside the frontend folder:
docker start -i appproject_web_1

docker-compose -f e2e-test.yml build
docker-compose -f e2e-test.yml up
docker-compose -f dev.yml build
docker-compose -f dev.yml up
