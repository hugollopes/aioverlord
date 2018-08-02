import os

os.system("kubectl config set-context minikube --namespace=e2e-topology-feature")
print("TEST=""$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"+ '"' + r"\n" + '"' + "}}{{end}}' | grep ^chrome)""")
os.system(
        "TEST=""$(kubectl get pods -o go-template --template '{{range .items}}{{.metadata.name}}{{"+ '"' + r"\n" + '"' +
        "}}{{end}}' | grep ^chrome)"";echo ${TEST};kubectl port-forward --pod=${TEST}  5901:5900")
#os.system("echo ${TEST}")
#os.system("kubectl port-forward --pod=${TEST}  5901:5900")