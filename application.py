import os
from flask import Flask, request, session, render_template, redirect
from flask_session import Session
from flask_socketio import SocketIO, emit
from datetime import datetime
from random import randint


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
all_channels = ['Default_Channel_1', 'channel2', 'channel3']

# all messages in all channels
messages_all_channels = [
	{
		"Channel_Name": "Default_Channel_1",
		"Channel_Messages": [
			{
				"UserName": "Junaid",
				"MessageText": "Hello Arsalan",
				"TimeStamp": "5 March 2020"
			},
			{
				"UserName": "Arsalan",
				"MessageText": "Hello Junaid",
				"TimeStamp": "6 March 2020"
			}
		]
	},
	{
		"Channel_Name": "Default_Channel_2",
		"Channel_Messages": [
			{
				"UserName": "Junaid",
				"MessageText": "Hello Arsalan",
				"TimeStamp": "5 March 2020"
			},
			{
				"UserName": "Junaid",
				"MessageText": "Hello Arsalan",
				"TimeStamp": "5 March 2020"
			}
		]
	}
]

# all messages in all persons chats
Messages_all_persons = {}




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
    session["username"] = ""
    print(session["session_id"])
    print(session["username"])

    if request.method == "GET":
        # if user already loggedin
        if session["session_id"] > 0:
            return redirect("/main")
    # if user not loggedin
        else:
            print(session["session_id"])
            print(session["username"])
            return render_template("login.html")

    # if post request
    elif request.method == "POST":

        # if user already loggedin
        if session["session_id"] > 0:
            print(session["session_id"])
            print(session["username"])
            return redirect("/main")
    # when user added username and press submit button
        else:
            username = request.form.get("username_from_form")
            if username in all_users:
                return render_template("login.html", javascript_alert="Username Already exists! Please choose another one!")
            else:                
                session["username"] = username
                session["session_id"] = randint(1, 99)
                all_users.append(username)
                print(session["session_id"])
                print(session["username"])
                return redirect("/main")


# default page
@app.route("/main", methods=["GET", "POST"])
def main():      
    print(session["session_id"])
    print(session["username"])          
    larger = find_larger(all_users, all_channels)
    print(all_users)
    return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger)

@app.route("/channel_create", methods=["POST"])
def channel_create():
    print(session["session_id"])
    print(session["username"])
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
    print(session["session_id"])
    print(session["username"])
  #  print(session["username"])
    #    if session["username"] != "":
    return render_template("channel.html")
 #   else:
 #   return redirect("/login")



@app.route("/channels/<string:channel>", methods=['GET', 'POST'])
def channels(channel):
    print(session["session_id"])
    print(session["username"])
#  print(type(channel))
 #   print(channel)
    channel_all_messages = {}
    channel_dict = {}
    #i for i, d in enumerate(listofpeople) if "Jack" in d.keys()
    channel_index = [i for i, d in enumerate(messages_all_channels) if channel in d.values()]
#    print(channel_index)
    #value_index = 0

    channel_dict = (messages_all_channels[channel_index[0]])
    print(channel_dict)

    for key1 in channel_dict:
        if key1 == "Channel_Messages":
            for items in channel_dict[key1]:
                print(items)
#                 channel_all_messages = key2
#                 channel_all_messages.update
        #print(d)
   # print(channel_dict[messages_index])

    return render_template("channel.html", channel=channel, all_channels = messages_all_channels, channel_all_messages = channel_all_messages)

@app.route("/people/<string:person>", methods=['GET', 'POST'])
def people(person):
    print(session["session_id"])
    print(session["username"])
    return render_template("people.html", person=person)





@socketio.on("submit vote")
def vote(data):
    username = session["username"]
    selection = data["selection"]
    full_date = datetime.now()
    message_time = str(full_date.hour)+" "+str(full_date.minute)
    print(type(data))
    print(selection)
    print(message_time)
    emit("announce vote", {"selection": selection,
                           "username": username,
                           "time": message_time}, broadcast=True)


@app.route("/logout", methods=["GET", "POST"])
def logout():
    print("logging out")
    print(session["session_id"])
    print(session["username"])
    session["session_id"] = 0
    session["username"] = ""
    return redirect("/login")



if __name__ == "__main__":
    socketio.run(app, debug=True)
