# aioverlord

playground project for multiple technologies

# Technologies

* machine learning / reinforment learning
* tensorflow
* python
* kubernetes
* vuejs
* nightjs/cucumber
* mongodb

# Requirements for dev env

* Linux ubunto(scripts should workrk in other versions as well)
* python3
* k8 (minikube for dev env)
* localhost docker registry in port 5000

# Instalation/run

* in /kubernetes/kubernetesdev/web-deployment.yaml  and /kubernetes/kubernetese2e/orig/web-deployment.yaml  ,replace the volume path with the abolute path in your work env., eg "/home/hugo/Projects/aioverlord/aioverlord-frontend" . this enables the changing web code without docker deploy. task to delocalize is pending
* run: "gradle build"  to build all the artifacts
* run: "gradle rundev"  for a dev instance.
* run: run2e2.py for running the test suit.

# Debug

* for checkin a feature test in vnc, run: python3 rune2e.py world vnc








