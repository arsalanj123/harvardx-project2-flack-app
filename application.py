import os
from flask import Flask, request, session, render_template, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit
from datetime import datetime


# Flask Application config
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
app.debug = Flask
socketio = SocketIO(app)

# Session configuration
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = 'filesystem'
Session(app)

# Socket

all_users = ['user1', 'user2']
all_channels = ['channel1', 'channel2', 'channel3']


def find_larger(lst1, lst2):

    if len(lst1) > len(lst2):
        larger = "list1"
    else:
        larger = "list2"
    return larger



@app.route("/login", methods=["GET", "POST"])
def index():

    # session check
    session["session_id"] = 0
    print(session["session_id"])

    if request.method == "GET":
        # if user already loggedin
        if session["session_id"] > 0:
            return redirect("/main")
    # if user not loggedin
        else:
            return render_template("login.html")

    # if post request
    elif request.method == "POST":

        # if user already loggedin
        if session["session_id"] > 0:
            return redirect("/main")
    # when user added username and press submit button
        else:
            username = request.form.get("username_from_form")
            if username in all_users:
                return render_template("login.html", javascript_alert="Username Already exists! Please choose another one!")
            else:                
                session["username"] = username
                all_users.append(username)
                print(username)
                return redirect("/main")


# default page
@app.route("/main", methods=["GET", "POST"])
def main():                
    larger = find_larger(all_users, all_channels)
    print(all_users)
    return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger)

@app.route("/channel_create", methods=["POST"])
def channel_create():
    
    new_channel_to_create = request.form.get("new_channel_from_form")
    
    if new_channel_to_create in all_channels:
        larger = find_larger(all_users, all_channels)
        return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger, javascript_alert="The Channel already exists!")
    
    else:
        all_channels.append(new_channel_to_create)
        larger = find_larger(all_users, all_channels)
        print(all_users)
        return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger)

# channel page
@app.route("/channel", methods=["GET", "POST"])
def channel():
  #  print(session["username"])
    #    if session["username"] != "":
    return render_template("channel.html")
 #   else:
 #   return redirect("/login")


@app.route("/channels/<string:channel>", methods=['GET', 'POST'])
def channels(channel):
    return render_template("channel.html", channel=channel)

@app.route("/people/<string:person>", methods=['GET', 'POST'])
def people(person):
    return render_template("people.html", person=person)





@socketio.on("submit vote")
def vote(data):
    username = session["username"]
    selection = data["selection"]
    print(type(data))
    print(selection)
    emit("announce vote", {"selection": selection,
                           "username": username}, broadcast=True)


if __name__ == "__main__":
    socketio.run(app, debug=True)
