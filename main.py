import datetime
import json
from re import U
import sqlite3

import flask
import hashlib

from flask import render_template, request
from flask_cors import CORS

app = flask.Flask(__name__)
CORS(app)

users = []
messages = {0: ""}
mid = 0


conn = sqlite3.connect(database="chat.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL, registration_date TEXT)")
conn.commit()
conn.close()


@app.route('/', methods=['POST', 'HEAD', 'GET'])
def index():
    global mid

    print(flask.request)

    if flask.request.method == 'GET':
        return render_template("index.html")

    if flask.request.method == 'POST':
        data = request.form['all_data']
        print(data)
        data = json.loads(data)
        
        
        if data["subject"] == "login":
            resp = loginuser(data)
            return resp


        elif data["subject"] == "sendmsg":
            mid += 1
            messages[mid] = data["message"]
            return " "

        elif data["subject"] == "getmsg":
            msg = {"message": messages[mid], "mid": mid}
            return json.dumps(msg)

        elif data["subject"] == "register":
            resp = registeruser(data)
            return resp

        else:
            return "error"


@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/chat",methods=["POST"])
def chat():
    u = request.form['uname']
    return render_template("chat.html",uname=u)

@app.route("/logout")
def logout():
    u = request.form['uname']
    users.remove(u)
    return render_template("index.html")

def registeruser(data):
    conn = sqlite3.connect(database="chat.db")
    cur = conn.cursor()
    firstname = data["fname"]
    lastname = data["lname"]
    username = data["uname"]
    password = data["passwd"]

    cur.execute("SELECT * FROM users WHERE username =?", (username,))
    records = cur.fetchall()
    if len(records) != 0:
        return "already"
    else:
        try:
            now = datetime.datetime.now()
            cur.execute(
                "INSERT INTO users (first_name, last_name, username, password,registration_date) VALUES (?, ?, ?, ?, ?)",
                (firstname, lastname, username, str(hashlib.md5(password.encode()).hexdigest()), now))
            conn.commit()
            conn.close()
            return "success"
        except Exception as e:
            print("Error while inserting the new record :", repr(e))
            return "failure"

def loginuser(data):
    conn = sqlite3.connect(database="chat.db")
    cur = conn.cursor()
    username = data["uname"]
    password = data["passwd"]

    cur.execute("SELECT username FROM users WHERE username =?",(username,))
    records = cur.fetchall()
    

    if len(records) == 0:
        conn.close()
        return "nouser"
        
    else:
        cur.execute("SELECT username FROM users WHERE username =? AND password=?",(username,hashlib.md5(password.encode()).hexdigest()))
        records = cur.fetchall()
        if(len(records) == 0):
            conn.close()
            return "badpasswd"

        else:
            conn.close()
            users.append(username)
            return "success"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True, threaded=True)
