import os
from flask import Flask, request, session, render_template
from flask_session import Session
#from flask_socketio import emit, SocketIO

#Flask Application config
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.debug = Flask

#Socket
#socketio = SocketIO(app)

#Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)


@app.route("/", methods=["GET","POST"])
def index():
    #session check
    session["session_id"] = 0
    print(session["session_id"])

    if request.method == "GET":
    #if session already in work
        if session["session_id"] > 0:
            return render_template("hompage.html")
    #if session not present 
        else:
            return render_template("login.html")


    elif request.method == "POST":
        if session["session_id"] > 0:
    #if session already in work
            return render_template("hompage.html")
    #if session not present, signup
    # Add user   
        else:
            return render_template("hompage.html")


@app.route("/navbar", methods=["GET","POST"])
def navbar():
    return render_template("navbar.html")


@app.route("/test", methods=["GET","POST"])
def test():
    return render_template("test.html")
