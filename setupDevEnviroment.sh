#!/usr/bin/env bash
# script to initialize dev environment

# to solve a dns related to ubuntu issue with had to do this:
# https://kubernetes.io/docs/tasks/administer-cluster/dns-debugging-resolution/
# https://github.com/kubernetes/minikube/issues/2027 --- see down
sudo sysctl net.ipv4.tcp_fin_timeout=30
sudo sysctl net.ipv4.ip_local_port_range="15000 61000"

if [ "$(pidof systemd)" ]; then
	SYSTEMD=true
else
	SYSTEMD=false
fi

if [ "$SYSTEMD" == "true" ]; then
	sudo sed -i -e 's/^#*.*DNSStubListener=.*$/DNSStubListener=no/' /etc/systemd/resolved.conf
	sudo sed -i -e 's/nameserver 127.0.1.1/nameserver 8.8.8.8/' /etc/resolv.conf

	systemctl is-active systemd-resolved >& /dev/null && sudo systemctl stop systemd-resolved
	systemctl is-enabled systemd-resolved >& /dev/null && sudo systemctl disable systemd-resolved

	sudo systemctl stop systemd-resolved
	sudo systemctl disable systemd-resolved
fi

sudo minikube stop
sudo minikube delete

if [ "$SYSTEMD" == "true" ]; then
	sudo minikube start --vm-driver=none
else
	# minikube always assumes systemd crap exists. bootstraper localkube is the proper way without nasty dependencies
	# adding path of the resolvconf, since /etc/resolv.conf is usually a symlink
	sudo minikube start --vm-driver=none --bootstrapper=localkube --extra-config=kubelet.resolv-conf=/var/run/resolvconf/resolv.conf -v 0
fi

sudo kubectl create -f https://raw.githubusercontent.com/kubernetes/dashboard/master/src/deploy/recommended/kubernetes-dashboard.yaml

sudo kubectl proxy &
disown

# no credentials in code
DOCKERHUB_USR=$(cat ~/secrets/GITHUB_USR.txt)
DOCKERHUB_PWD=$(cat ~/secrets/GITHUB_PWD.txt)

docker login -p "$DOCKERHUB_PWD" -u "$DOCKERHUB_USR"
#restarting registry if needed
docker run -d -p 5000:5000 --restart=always --name registry registry:2

#example build code... should be jenkins/grunt
#  docker build  ./aioverlord-frontend/  --tag nathor/frontend:latest
#  docker tag 45cdb98cc93d nathor/backend:latest
#  docker push nathor/frontend:latest
#  docker push nathor/backend:latest
# kubectl get ep/web -o jsonpath="{.subsets[0].addresses[0].ip}"
# kubectl get ep/web -o jsonpath="{.subsets[0].ports[0].port}"

#echo web address
# echo  "$(kubectl get ep/web -o jsonpath='{.subsets[0].addresses[0].ip}'):$(kubectl get ep/web -o jsonpath='{.subsets[0].ports[0].port}')"
#echo  "$(kubectl get ep/flask -o jsonpath='{.subsets[0].addresses[0].ip}'):$(kubectl get ep/flask -o jsonpath='{.subsets[0].ports[0].port}')"




