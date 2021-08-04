from datetime import date, datetime
from flask import Flask, request, jsonify, make_response, redirect, url_for
import json
import gevent.pywsgi


app = Flask(__name__)
port = 8080

@app.route('/status', methods=['GET'])
def status():
  return "I'm alive.", 200

@app.route("/webhook", methods=['POST'])
def webhook():
  alertFromAlertmanager = request.json
  #print("Incoming JSON:", alertFromAlertmanager)
  print(json.dumps(alertFromAlertmanager))
  
  return {
    "mensaje": "recepcionado y devuelto",
    "varAlertFromAlertmanager": alertFromAlertmanager
    }

if __name__ == '__main__':
  #DEVEL
  #app.run(host="0.0.0.0", port=8080)
  app_server = gevent.pywsgi.WSGIServer((port), app)
  app_server.serve_forever()