#!/usr/bin/env bash


i=1
until (curl -s "http://localhost:8001/api/v1/namespaces/default/services/flask/proxy/#/" --max-time 1 | grep "db connection active") #curl http://localhost:8001/api/v1/namespaces/default/services/flask/proxy/#/
do
	echo "try $i times."
	i=$(( i+1 ))
	sleep 2
done

until (curl -s "http://localhost:8001/api/v1/namespaces/default/services/web/proxy/#/" --max-time 1 | grep "html") #curl http://localhost:8001/api/v1/namespaces/default/services/flask/proxy/#/
do
	echo "try $i times."
	i=$(( i+1 ))
	sleep 2
done



