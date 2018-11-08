#! /usr/bin/env python3 

from flask import Flask, request

app = Flask(__name__)


@app.route("/", methods=["POST", "GET"])
def hello():
    if request.method == "POST":
        return "Nothing to post!\n"
    else:
        return "Hello World!\n"


if __name__ == "__main__":
    app.run()
