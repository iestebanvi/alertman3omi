from datetime import date, datetime
from flask import Flask, request, jsonify, make_response, redirect, url_for
import json

app = Flask(__name__)

@app.route('/status', methods=['GET'])
def status():
  return "I'm alive.", 200

@app.route('/', methods=['GET'])
def root():
    return redirect(url_for('status'))

@app.route("/webhook", methods=['POST'])
def webhook():
  alertFromAlertmanager = request.json
  print("Incoming JSON:", alertFromAlertmanager)
  reformatedRequestJson = json.dumps(alertFromAlertmanager) 
  print("Incoming JSON Reformated", reformatedRequestJson)

  return {"mensaje": "recepcionado y devuelto"}


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8080, debug=True)
    