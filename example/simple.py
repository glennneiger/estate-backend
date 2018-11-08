#! /usr/bin/env python3 

import sys
import json
from flask import Flask, request

app = Flask(__name__)


def is_browser(ua_string):
    return ua_string.split('/')[0].lower() == 'mozilla'


@app.route("/")
def hello():
    msg_content = "Hello World!"
    if is_browser(request.headers['User-Agent']):
        return "<html><body><h1>{}</body></html>".format(msg_content)

    else:
        response = dict()
        response["msg"] = msg_content
        return json.dumps(response)


@app.route("/name", methods=["POST"])
def greeting():
    print(request.data, file=sys.stdout)
    req = json.loads(request.data)
    req["msg"] = "Hi, {}".format(req["name"])
    return json.dumps(req)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(sys.argv[1]))
