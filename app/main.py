#! /usr/bin/env python3 

from flask import Flask, request, make_response, jsonify

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        return jsonify({'fulfillmentText': "post received"})
    else:
        return jsonify({'fulfillmentText': "get received"})
