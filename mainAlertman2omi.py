from datetime import date, datetime
from flask import Flask, request, jsonify, make_response, redirect, url_for
import json

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
  return "I'm alive.", 200

@app.route("/webhook", methods=['POST'])
def webhook():
  alertFromAlertmanager = request.json
  #print(json.dumps(alertFromAlertmanager))
  print("Incoming JSON: ", json.dumps(alertFromAlertmanager))
  
  return {
    "mensaje": "recepcionado y devuelto",
    "varAlertFromAlertmanager": alertFromAlertmanager
    }

if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8080)
