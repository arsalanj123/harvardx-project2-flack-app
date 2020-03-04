import os
from flask import Flask, request, session, render_template, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit
from datetime import datetime


#Flask Application config
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.debug = Flask
socketio = SocketIO(app)

#Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

#Socket

@app.route("/login", methods=["GET","POST"])
def index():

    #session check
    session["session_id"] = 0
    print(session["session_id"])

    if request.method == "GET":
    #if user already loggedin
        if session["session_id"] > 0:
            return redirect("homepage.html")
    #if user not loggedin 
        else:
            return render_template("login.html")

    #if post request
    elif request.method == "POST":
        
        # if user already loggedin
        if session["session_id"] > 0:
            return render_template("hompage.html")
    # when user added username and press submit button
        else:
            username = request.form.get("username_from_form")
            session["username"] = username
            print(username)
            return render_template("homepage.html")            


#default page
@app.route("/main", methods=["GET","POST"])
def main():
    return render_template("homepage.html")

#channel page
@app.route("/channel", methods=["GET","POST"])
def channel():
  #  print(session["username"])
#    if session["username"] != "":
    return render_template("channel.html")
 #   else:
 #   return redirect("/login")

@socketio.on("submit vote")
def vote(data):
    username = session["username"]
    selection = data["selection"]
    print(type(data))
    print(selection)
    emit("announce vote", {"selection": selection, "username": username}, broadcast=True)

if __name__ == "__main__":
    socketio.run(app, debug=True)