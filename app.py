import concurrent.futures
import datetime
import hashlib
import json
from pydoc import render_doc
import re
import sqlite3
from uuid import uuid4
import flask
from User import Users

app = flask.Flask(__name__)
users = {}
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

conn = sqlite3.connect(database="chat.db")
cur = conn.cursor()
now = datetime.datetime.now()
try:
    cur.execute(
        "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, email TEXT NOT NULL UNIQUE, username TEXT NOT NULL "
        "UNIQUE, password TEXT NOT NULL,uuid TEXT NOT NULL UNIQUE, registration_date TEXT)")
    cur.execute("INSERT INTO users (email, username, password, uuid, registration_date) VALUES (?, ?, ?, ?, ?)",
                ("root@root.com", "root", str(hashlib.md5("root".encode()).hexdigest()), 77777777, now))
except:
    pass
finally:
    conn.commit()
    conn.close()
    del conn, now, cur


@app.route('/', methods=['POST', 'HEAD', 'GET'])
def index():
    global users

    if flask.request.method == 'GET':
        return flask.render_template("index.html")

    if flask.request.method == "HEAD":
        return flask.Response("")

    if flask.request.method == 'POST':
        try:
            data = flask.request.get_json()

            if data["subject"] == "login":
                resp = loginuser(data)
                return resp

            elif data["subject"] == "sendmsg":
                u = data["fromuser"]
                if users[u].getkey() == data["key"]:
                    user1 = data["fromuser"]
                    user2 = data["touser"]
                    res = send_msg(user1, user2, data["message"])
                    return res
                else:
                    return {"status": "bad key"}

            elif data["subject"] == "getmsg":
                try:
                    res = getmsg(data["fromuser"], data['touser'], data["key"])
                    return res
                except KeyError as e:
                    print(repr(e))
                    return {"status": "bad key"}

            elif data["subject"] == "register":
                resp = registeruser(data)
                return resp

            elif data["subject"] == "getusers":
                u = data["uname"]
                if users[u].getkey() == str(data['key']):
                    res = fetchusers()
                    r = {i: j for i, j in zip(range(len(res)), res)}
                    return r
                else:
                    return {"status": "bad key"}

            elif data["subject"] == "logout":
                res = logout(u=data["uname"], k=data["key"])
                return res

            elif data["subject"] == "chat":
                res = chat(t=data["to"], f=data["from"], k=data["key"])
                return res

            elif data["subject"] == "resetpass":
                # res = resetpass(uname, oldpass, newpass)
                # return res
                pass

            else:
                return {"status": "error"}
        except Exception as e:
            print(repr(e))
            return {"status": "bad request"}


@app.route("/register")
def register():
    return flask.render_template("register.html")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/chat", methods=["POST"])
def chat(t=None, f=None, k=None):
    if t is None:
        try:
            data = flask.request.form
            u = data["from"]
            if users[u].getkey() == str(data["key"]) and data["subject"] == "sendto":
                user1 = data['from']
                user2 = data['to']
                return flask.render_template("chat.html", uname=user1, touser=user2)
            else:
                return {"status": "bad data"}
        except Exception as e:
            print(repr(e))
            return {"status": "bad data"}

    else:
        try:
            if users[f].getkey() == str(k):
                return {"status": "success"}
        except Exception as e:
            print(repr(e))


@app.route("/logout", methods=["POST"])
def logout(u=None, k=None):
    if k is None:
        try:
            uname = flask.request.form['uname']
            if users[uname].getkey() == flask.request.form["key"]:
                un = users.pop(uname)
                del un
                return flask.redirect(flask.url_for("index"))
        except Exception as e:
            print(repr(e))
            return {"status": "bad request"}
    else:
        try:
            if users[u].getkey() == k:
                un = users.pop(u)
                del un
                return {"status": "logout"}
        except Exception as e:
            print(repr(e))
            return {"status": "error"}


@app.route('/interface', methods=["POST"])
def interface():
    try:
        u = flask.request.form["uname"]
        k = flask.request.form["key"]
        un = users[u].getkey()
        if k == users[u].getkey():
            return flask.render_template("interface.html", uname=u)
        else:
            return {"status": "bad key"}
    except Exception as e:
        print(repr(e))
        return {"status": "bad request"}


@app.route('/reset', methods=["GET"])
def reset():
    return flask.render_template("reset.html")


def resetpass(uname, oldpass, newpass):
    res = fetchusers()


def registeruser(data):
    conn = sqlite3.connect(database="chat.db")
    cur = conn.cursor()
    email = data["email"]
    username = data["uname"]
    password = data["passwd1"]

    if (5 > len(username) < 13) or " " in username:
        return {"status": "Username should be between 5 to 13 characters without spaces"}
    if (5 > len(password) < 20) or " " in password:
        return {"status": "password should be between 5 to 20 characters without spaces"}
    if not re.search(regex, email):
        return {"status": "Enter a valid email"}

    cur.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE", (username,))
    records = cur.fetchall()
    if len(records) != 0:
        return {"status": "alreadyuser"}
    else:
        cur.execute("SELECT * FROM users WHERE email =? COLLATE NOCASE", (email,))
        records = cur.fetchall()
        if len(records) != 0:
            return {"status": "alreadyemail"}

        try:
            now = datetime.datetime.now()
            userid = uuid4().hex
            cur.execute(
                "INSERT INTO users (email, username, password, uuid, registration_date) VALUES (?, ?, ?, ?, ?)",
                (email, username, str(hashlib.md5(password.encode()).hexdigest()), userid, now))
            conn.commit()
            conn.close()
            return {"status": "success"}
        except Exception as e:
            print("Error while inserting the new record :", repr(e))
            return {"status": "failure"}


def loginuser(data):
    username = ""
    try:
        username = data["uname"]
        password = data["passwd"]

        conn = sqlite3.connect(database="chat.db")
        cur = conn.cursor()
        cur.execute("SELECT username FROM users WHERE username =? COLLATE NOCASE", (username,))
        records = cur.fetchall()

        if len(records) == 0:
            conn.close()
            return {"status": "nouser"}

        else:
            username = records[0][0]
            cur.execute("SELECT uuid FROM users WHERE username =? COLLATE NOCASE AND password=?",
                        (username, hashlib.md5(password.encode()).hexdigest()))
            records = cur.fetchall()
            if len(records) == 0:
                conn.close()
                return {"status": "badpasswd"}

            else:
                uid = records[0][0]
                conn.close()
                try:
                    ret = users[username].getkey()

                except KeyError:
                    users[username] = Users(username, uid)
                    ret = users[username].getkey()

                print(ret)
                return {"status": "success", "key": ret, "uname": username}

    except KeyError:
        key = data["key"]

    try:
        if key and users[username].getkey() == key:
            un = users[username]
            uid = users[username].getid()
            del un
            users[username] = Users(username, uid)
            new_key = users[username].getkey()
            return {"status": "success", "key": new_key}
    except KeyError:
        return {"status": "incorrect"}


def send_msg(fromu, tou, msg):
    usr = fetchusers()
    if fromu in usr and tou in usr:
        try:
            user1, user2 = sortedstring(fromu.lower(), tou.lower())
            conn = sqlite3.connect(database="chat.db")
            cur = conn.cursor()
            cur.execute(
                f"CREATE TABLE IF NOT EXISTS {user1 + user2} (id INTEGER PRIMARY KEY,message TEXT,fromuser TEXT,date TEXT)")
            conn.commit()
            cur.execute(f"INSERT INTO {user1 + user2} (message,fromuser) VALUES (?,?)", (msg, fromu))
            conn.commit()
            conn.close()
            return {"status": "success"}
        except Exception as e:
            print(repr(e))
    else:
        return {"status": "bad username"}


def getmsg(user1, user2, key):
    if users[user1].getkey() == key:
        usr = fetchusers()
        if user1 in usr and user2 in usr:
            try:
                user1, user2 = sortedstring(user1.lower(), user2.lower())
                conn = sqlite3.connect(database="chat.db")
                cur = conn.cursor()
                cur.execute(f"SELECT message,fromuser FROM {user1 + user2}")
                res = cur.fetchall()
                conn.close()
                r1 = [res[i][0] for i in range(len(res))]
                r2 = [res[i][1] for i in range(len(res))]
                r = {"messages": r1, "user": r2}
                return r

            except Exception as e:
                print(repr(e))
                return {"status": "error"}
        else:
            return {"status": "bad username"}


def sortedstring(a, b):
    for i, j in zip(a, b):
        if i > j:
            return a, b
        elif i < j:
            return b, a

    return a,b

def fetchusers():
    conn = sqlite3.connect(database="chat.db")
    cur = conn.cursor()
    cur.execute("SELECT username FROM users")
    res = cur.fetchall()
    conn.close()
    res = [res[i][0] for i in range(len(res))]
    return res


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5005, debug=True, use_debugger=False, use_reloader=False)
