from datetime import date, datetime
from flask import Flask, request, jsonify, make_response, redirect, url_for
import json
import requests
from xml.etree import ElementTree as et

app = Flask(__name__)
xmlTemplate="""
<omi-event-message>
<title></title>
<description></description>
<severity></severity>
<node></node>
<object></object>
<category></category>
<subcategory></subcategory>
<affectedCI></affectedCI>
</omi-event-message>"""

@app.route('/status', methods=['GET'])
def status():
  return "I'm alive.", 200

@app.route("/webhook", methods=['POST'])
def webhook():
  alertFromAlertmanager = request.json
  #print(json.dumps(alertFromAlertmanager))
  print("Incoming JSON: ", json.dumps(alertFromAlertmanager))

# xml = """<?xml version='1.0' encoding='utf-8'?>
# <a>б</a>"""
# headers = {'Content-Type': 'application/xml'} # set what your server accepts
# print requests.post('http://httpbin.org/post', data=xml, headers=headers).text

  headers = {'Content-Type': 'application/xml'} # set what your server accepts
  data=et.parse(xmlTemplate)
  data.find('omi-event-message/title').text = 'Nueva Alarma'
  data.write(xmlTemplate)
  print ("data", data)
  
  
  return {
    "mensaje": "recepcionado y devuelto",
    "varAlertFromAlertmanager": alertFromAlertmanager
    }

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)
