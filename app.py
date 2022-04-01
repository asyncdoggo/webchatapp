import concurrent.futures
import datetime
import hashlib
import json
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

    if flask.request.method == 'POST':
        try:
            print(flask.request.form)
            data = flask.request.form['all_data']
            data = json.loads(data)

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
                    return "bad key"

            elif data["subject"] == "getmsg":
                try:
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(getmsg, data["fromuser"], data['touser'], data["key"])
                        return_value = future.result()
                        return return_value
                except KeyError:
                    return "bad key"

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
                    return "wrong key"

            else:
                return "error"
        except Exception as e:
            print(repr(e))
            return "bad request"


@app.route("/register")
def register():
    return flask.render_template("register.html")


@app.route("/login")
def login():
    return flask.render_template("login.html")


@app.route("/chat", methods=["POST"])
def chat():
    try:
        data = flask.request.form
        u = data["from"]
        if users[u].getkey() == str(data["key"]) and data["subject"] == "sendto":
            user1 = data['from']
            user2 = data['to']
            return flask.render_template("chat.html", uname=user1, touser=user2)
        else:
            return "bad data"
    except Exception as e:
        print(repr(e))
        return "bad data"


@app.route("/logout", methods=["POST"])
def logout():
    try:
        u = flask.request.form['uname']
        if users[u].getkey() == flask.request.form["key"]:
            un = users.pop(u)
            del un
            return flask.redirect(flask.url_for("index"))
    except Exception as e:
        print(repr(e))
        return "bad request"


@app.route('/interface', methods=["POST"])
def interface():
    try:
        u = flask.request.form["uname"]
        k = flask.request.form["key"]
        un = users[u].getkey()
        if k == users[u].getkey():
            return flask.render_template("interface.html", uname=u)
        else:
            return "bad key"
    except Exception as e:
        print(repr(e))
        return "bad request"


def registeruser(data):
    conn = sqlite3.connect(database="chat.db")
    cur = conn.cursor()
    email = data["email"]
    username = data["uname"]
    password = data["passwd1"]

    if (5 > len(username) < 13) or " " in username:
        return "Username should be between 5 to 13 characters without spaces"
    if (5 > len(password) < 20) or " " in password:
        return "password should be between 5 to 20 characters without spaces"
    if not re.search(regex, email):
        return "Enter a valid email"

    cur.execute("SELECT * FROM users WHERE username = ? COLLATE NOCASE", (username,))
    records = cur.fetchall()
    if len(records) != 0:
        return "alreadyuser"
    else:
        cur.execute("SELECT * FROM users WHERE email =? COLLATE NOCASE", (email,))
        records = cur.fetchall()
        if len(records) != 0:
            return "alreadyemail"

        try:
            now = datetime.datetime.now()
            userid = uuid4().hex
            cur.execute(
                "INSERT INTO users (email, username, password, uuid, registration_date) VALUES (?, ?, ?, ?, ?)",
                (email, username, str(hashlib.md5(password.encode()).hexdigest()), userid, now))
            conn.commit()
            conn.close()
            return "success"
        except Exception as e:
            print("Error while inserting the new record :", repr(e))
            return "failure"


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
            users[username] = Users(username,uid)
            new_key = users[username].getkey()
            return {"status": "success", "key": new_key}
    except KeyError:
        return "incorrect"


def send_msg(user1, user2, msg):
    usr = fetchusers()
    if user1 in usr and user2 in usr:
        try:
            user1, user2 = sortedstring(user1.lower(), user2.lower())
            conn = sqlite3.connect(database="chat.db")
            cur = conn.cursor()
            cur.execute(f"CREATE TABLE IF NOT EXISTS {user1 + user2} (id INTEGER PRIMARY KEY,message TEXT)")
            conn.commit()
            cur.execute(f"INSERT INTO {user1 + user2} (message) VALUES (?)", (msg,))
            conn.commit()
            conn.close()
            return "success"
        except:
            pass
    else:
        return "bad username"


def getmsg(user1, user2, key):
    if users[user1].getkey() == key:
        usr = fetchusers()
        if user1 in usr and user2 in usr:
            try:
                user1, user2 = sortedstring(user1.lower(), user2.lower())
                conn = sqlite3.connect(database="chat.db")
                cur = conn.cursor()
                cur.execute(f"SELECT message FROM {user1 + user2}")
                res = cur.fetchall()
                conn.close()
                res = [res[i][0] for i in range(len(res))]
                r = {i: j for i, j in zip(range(len(res)), res)}
                return r

            except Exception as e:
                print(repr(e))
                return "error"
        else:
            return "bad username"


def sortedstring(a, b):
    f = 0
    for i, j in zip(a, b):
        if i > j:
            f = 1
            break
        elif i < j:
            f = 0
            break

    if f:
        return a, b
    else:
        return b, a


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
