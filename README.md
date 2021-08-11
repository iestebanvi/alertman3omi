# alertman3omi


#Proyecto para convertir las alarmas que vienen de alertmanager a OMI/OBM.
## Deploy de la aplicaicon omiReceiver en Openshift
oc new-app https://github.com/iestebanvi/alertman3omi --context-dir=omiReceiver/app --name=omieceiver
## Deploy de la aplicaicon alertman2omi en Openshift
oc new-app https://github.com/iestebanvi/alertman3omi --context-dir=alertman2omi/app --name=alertman2omi
## Start de Build de
oc start-build alertman3omi

curl -i -H "Accept: application/json" -H "Content-Type: application/json" -X GET http://alertman2omi-alertman3omi.apps.ocp4poc.example.com/status -v

curl -X PUT -H "Content-Type: application/json" -d '{"name":"mkyong","email":"abc@gmail.com"}' http://alertman2omi-alertman3omi.apps.ocp4poc.example.com/webhook -v



curl --header "Content-Type: application/json"   --request POST   --data '{"receiver": "webhook_omi", "status": "firing", "alerts": [{"status": "firing", "labels": {"alertname": "UpdateAvailable", "channel": "stable-4.6", "endpoint": "metrics", "instance": "192.168.20.55:9099","job": "cluster-version-operator", "namespace": "openshift-cluster-version", "pod": "cluster-version-operator-86bc8c9d94-rzhhn", "prometheus": "openshift-monitoring/k8s", "service":"cluster-version-operator", "severity": "info", "upstream": "https://api.openshift.com/api/upgrades_info/v1/graph"}, "annotations": {"message": "Your upstream update recommendation service recommends you update your cluster.  or https://console-openshift-console.apps.ocp4poc.example.com/settings/cluster/."}, "startsAt": "2021-08-03T21:26:16.457Z", "endsAt": "0001-01-01T00:00:00Z", "generatorURL": "https://prometheus-k8s-openshift-monitoring.apps.ocp4poc.example.com/graph?g0.expr=cluster_version_available_updates+%3E+0&g0.tab=1", "fingerprint": "2ffa08f8d1d462e9"}],  "truncatedAlerts": 0}'   http://alertman2omi-alertman3omi.apps.ocp4poc.example.com/webhook -vvvv

