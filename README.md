# alertman3omi




[root@bastionk8s ~]# oc new-app https://github.com/iestebanvi/alertman3omi --context-dir=omiReceiver/app --name=omieceiver
[root@bastionk8s ~]# oc new-app https://github.com/iestebanvi/alertman3omi --context-dir=alertman2omi/app --name=alertman2omi
[root@bastionk8s ~]# oc start-build alertman3omi

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://alertman2omi-alertman3omi.apps.ocp4poc.example.com/status -v

curl -X PUT -H "Content-Type: application/json" -d '{"name":"mkyong","email":"abc@gmail.com"}' http://alertman2omi-alertman3omi.apps.ocp4poc.example.com/webhook -v
