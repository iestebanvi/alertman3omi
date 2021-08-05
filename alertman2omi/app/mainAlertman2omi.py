#from datetime import date, datetime
from flask import Flask, request, jsonify, make_response, redirect, url_for
import json
import requests
from xml.etree import ElementTree as ET
import os
import sys

app = Flask(__name__)
xmlTemplate="""<omi-event-message><title></title><description></description><severity></severity><node></node><object></object><category></category><subcategory></subcategory><affectedCI></affectedCI></omi-event-message>"""

try:
    ENV_URL = os.environ.get("OMI_URL", "http://127.0.0.1:8080/postomi")
    ENV_CATEGORY = os.environ.get("OMI_CATEGORY", "OMI_CATEGORYOOCP4")
    ENV_HOSTNAMECI = os.environ.get("OMI_CI", "HOSTNAME_ocp4")
except Exception as ex:
    print('Something is wrong with config env vars OMI_URL, OMI_CATEGORY, OMI_CI: {}'.format(ex))
    sys.exit(1)

# {'Content-type': 'text/xml'}
# <omi-event-message>
#   <title>Watchdog</title>  ---> alertname
#   <description>This is an alert meant to ensure that the entire alerting pipeline is functional.       ----> "annotations": {"message":
# This alert is always firing, therefore it should always be firing in Alertmanager
# and always fire against a receiver. There are integrations with various notification
# mechanisms that send a notification when this alert is not firing. For example the
# &#34;DeadMansSnitch&#34; integration in PagerDuty.
# </description>
#   <severity>normal</severity>    --->  if watchdog > severity normal else critical
#   <node></node>
#   <object></object>
#   <category>INCIDENT</category>      -----> ini_category = os.environ.get("OMI_CATEGORY", "OPENSHIFT")
#   <subcategory>Watchdog</subcategory>    -> 
#   <affectedCI>ocpsalut</affectedCI>     ->     ini_affectedCI = os.environ.get("OMI_CI", "ocp4")
# </omi-event-message>


@app.route('/status', methods=['GET'])
def status():
  return "I'm alive.", 200

@app.route("/webhook", methods=['POST'])
def webhook():
  compactAlert=""
  alertFromAlertmanager = request.json
  print("Incoming JSON: <<<<<<  ", json.dumps(alertFromAlertmanager))
  print ("........")

  #Compactamos todas las alerts si en un POST vienen agrupadas en un array
  for alert in alertFromAlertmanager['alerts']:
    if alert != alertFromAlertmanager['alerts'][-1]:  # Miramos si es el ultmo para no pintar '|'
      compactAlert = compactAlert + alert['annotations']['message'] + "|"
    else:
      compactAlert = compactAlert + alert['annotations']['message']

  data = ET.fromstring(xmlTemplate)

  #data.find('.//title').text = alertFromAlertmanager['alerts'][0]['labels']['alertname']
  data.find('title').text = alertFromAlertmanager['alerts'][0]['labels']['alertname']
  data.find('description').text = compactAlert
  data.find('severity').text = 'critical'
  if alertFromAlertmanager['alerts'][0]['labels']['alertname'] == 'Watchdog':
    data.find('severity').text = 'normal'
  data.find('node').text = ENV_HOSTNAMECI
  data.find('category').text = ENV_CATEGORY
  data.find('subcategory').text = alertFromAlertmanager['alerts'][0]['labels']['alertname']
  data.find('affectedCI').text = ENV_HOSTNAMECI

  finalXML=ET.tostring(data, encoding='unicode', method='xml')  # Ponemos Unixcode para luego poder hacer el return del JSON final
  HEADERS = {'Content-Type': 'application/xml'}

  print ("SEND TO OMI >>>>> , ENV_URL: ", ENV_URL," HEADERS: ", HEADERS," finalXML: ",finalXML)

  try:
    response = requests.post(ENV_URL, headers=HEADERS, data=finalXML)
  except requests.exceptions.RequestException as errorpost:
    print ("ERROR en la conexion con OMI. Revisar Agente de OMI en servidor:", ENV_URL)
    raise SystemExit(errorpost)
    
  return {
    "ResumenMensajes": {
      "Incoming JSON: ": json.dumps(alertFromAlertmanager),
      "SEND TO OMI":{
        "ENV_URL": ENV_URL,
        "HEADERS": HEADERS,
        "finalXML": finalXML
        }
      }
    }, response.status_code


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)
