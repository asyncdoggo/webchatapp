import datetime
import json
import sqlite3
from uuid import uuid4

import flask
import hashlib

from flask import render_template, request
from flask_cors import CORS

from User import Users

app = flask.Flask(__name__)
CORS(app)

users = {}
messages = {0: ""}
mid = 0


conn = sqlite3.connect(database="chat.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, first_name TEXT NOT NULL, last_name TEXT NOT NULL, username TEXT NOT NULL UNIQUE, password TEXT NOT NULL,uuid TEXT NOT NULL UNIQUE, registration_date TEXT)")
conn.commit()
conn.close()


@app.route('/', methods=['POST', 'HEAD', 'GET'])
def index():
    global mid,users

    if flask.request.method == 'GET':
        return render_template("index.html")

    if flask.request.method == 'POST':
        try:
            print(request.form)
            data = request.form['all_data']
            data = json.loads(data)
            
            
            if data["subject"] == "login":
                resp = loginuser(data)
                return resp


            elif data["subject"] == "sendmsg":
                u = data["fromuser"] 
                if users[u].getkey() == data["key"]:
                    user1 = data["fromuser"]
                    user2 = data["touser"]
                    res = send_msg(user1,user2,data["message"])
                    return res
                else:
                    return "bad key"

            elif data["subject"] == "getmsg":
                u = data["fromuser"] 
                if users[u].getkey() == data["key"]:
                    res = getmsg(data["fromuser"],data['touser'])
                    return res 
                else:
                    return "bad key"

            elif data["subject"] == "register":
                resp = registeruser(data)
                return resp

            elif data["subject"] == "getusers":
                u = data["uname"]
                if users[u].getkey() == str(data['key']):
                    res=fetchusers()
                    r = {i:j for i,j in zip(range(len(res)),res)}
                    return r
                else:
                    return "wrong key"

                

            else:
                return "error"
        except Exception as e:
            print(repr(e))
            return "bad request"

@app.route("/register")
def register():
    return render_template("register.html")


@app.route("/login")
def login():
    return render_template("login.html")

@app.route("/chat",methods=["POST"])
def chat():
    try:
        data = request.form
        u = data["from"]
        if users[u].getkey() == str(data["key"]) and data["subject"] == "sendto":
            user1 = data['from']
            user2 = data['to']
            return render_template("chat.html",uname=user1,touser=user2)
        else:
            return "bad data"
    except Exception as e:
        print(repr(e))
        return "bad data"

@app.route("/logout",methods=["POST"])
def logout():
    try:
        u = request.form['uname']
        if users[u].getkey() == request.form["key"]:
            un = users.pop(u)
            del un
            return render_template("index.html")
    except Exception as e:
        print(repr(e))
        return "bad request"


@app.route('/interface',methods=["POST"])
def interface():
    try:
        u = request.form['uname']
        k = request.form["key"]

        if k == users[u].getkey():
            return render_template("interface.html",uname=u)
        else:
            return "bad key"
    except Exception as e:
        print(repr(e))
        return "bad request"

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
            userid = uuid4().hex
            cur.execute(
                "INSERT INTO users (first_name, last_name, username, password, uuid, registration_date) VALUES (?, ?, ?, ?, ?, ?)",
                (firstname, lastname, username, str(hashlib.md5(password.encode()).hexdigest()),userid, now))
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
        return {"status":"nouser"}

        
    else:
        cur.execute("SELECT uuid FROM users WHERE username =? AND password=?",(username,hashlib.md5(password.encode()).hexdigest()))
        records = cur.fetchall()
        if(len(records) == 0):
            conn.close()
            return {"status":"badpasswd"}

        else:
            id = records[0][0]
            conn.close()
            ret = ""
            try:
                ret = users[username].getkey()
            
            except:
                e = Users(username,id)
                ret = e.getkey()
                users[username] = e
                
            print(ret)
            return {"status":"success","key":ret}

def send_msg(user1,user2,msg):
    usr = fetchusers()
    if user1 in usr and user2 in usr:
        try:
            user1,user2 = sortedstring(user1,user2)
            conn = sqlite3.connect(database="chat.db")
            cur = conn.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {user1+user2} (id INTEGER PRIMARY KEY,message TEXT)")
            conn.commit()
            cur.execute(f"INSERT INTO {user1+user2} (message) VALUES (?)",(msg,))
            conn.commit()
            conn.close()
            return "success"
        except:
            pass
    else:
        return "bad username"

def getmsg(user1,user2):
    usr = fetchusers()
    if user1 in usr and user2 in usr:
        try:
            user1,user2 = sortedstring(user1,user2)
            conn = sqlite3.connect(database="chat.db")
            cur = conn.cursor()
            cur.execute(f"SELECT message FROM {user1+user2}")
            res = cur.fetchall()
            conn.close()
            res = [res[i][0] for i in range(len(res))]
            r = {i:j for i,j in zip(range(len(res)),res)}
            return r

        except Exception as e:
            print(repr(e))
            return "error"
    else:
        return "bad username"



def sortedstring(a,b):
    f = 0
    for i,j in zip(a,b):
        if i>j:
            f = 1
            break
        elif i<j:
            f = 0
            break

    if f:
        return a,b
    else:
        return b,a

def fetchusers():
    conn = sqlite3.connect(database="chat.db")
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    res = cur.fetchall()
    conn.close()
    res = [res[i][0] for i in range(len(res))]
    return res

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True)
