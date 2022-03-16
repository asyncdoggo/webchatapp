import datetime
import json
from pyexpat.errors import messages
import sqlite3
from concurrent.futures import ThreadPoolExecutor
from urllib import response

import flask
import hashlib

from flask import render_template, request
from werkzeug.wrappers import Response
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

users = []
messages = {}
mid = 0


@app.route('/', methods=['POST', 'HEAD', 'GET'])
def index():
    global mid

    print(flask.request)

    if flask.request.method == 'GET':
        return render_template("index.html")

    if flask.request.method == 'POST':
        data = request.form['all_data']
        data = json.loads(data)

        if data['subject'] == 'login':
            return data['username']

        elif data["subject"] == "sendmsg":
            mid += 1
            messages[mid] = data["message"]
            return " "

        elif data["subject"] == "getmsg":
            msg = {"message":messages[mid],"mid":mid}
            return json.dumps(msg)

        else:
            return "error"


@app.route("/<uname>")
def chat(uname):
    print(uname)
    if uname in users:
        return render_template("index.html",error="Username is taken")
    else:
        users.append(uname)
        return render_template("chat.html",uname=uname)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True, threaded=True)
