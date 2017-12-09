#!/usr/bin/env bash
#docker build
docker build -t flask .

#docker run
docker run -p 5000:5000 flask
docker run --name mongodb -d -p 27017:27017 mongo:3.5

