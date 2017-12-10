#!/usr/bin/env bash
#docker build
docker-compose -f dev.yml build
docker-compose -f dev.yml up
