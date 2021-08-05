#from datetime import date, datetime
from flask import Flask, request, jsonify, make_response, redirect, url_for
import sys

app = Flask(__name__)

@app.route('/postomi', methods=['POST'])
def status():
  print("Result: \n%s\n" % request.data, file=sys.stderr)
  return "Result: \n%s\n" % request.data, 200


if __name__ == '__main__':
  app.run(host="0.0.0.0", port=8081)
