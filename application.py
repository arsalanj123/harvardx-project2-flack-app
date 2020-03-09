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

all_users = ['default_user_1', 'default_user_2']
all_channels = ['Default_Channel_1', 'Default_Channel_2']

# all messages in all channels
messages_all_channels = [
    {
        "Channel_Name": "Default_Channel_1",
        "Channel_Messages": [
            {
                        "UserName": "default_user_1",
                        "MessageText": "Yo people!",
                "TimeStamp": "17 11"
            },
            {
                "UserName": "default_user_2",
                "MessageText": "Heylo everyone, good morning!",
                "TimeStamp": "17 11"
            }
        ]
    },
    {
        "Channel_Name": "Default_Channel_2",
        "Channel_Messages": [
            {
                        "UserName": "default_user_2",
                        "MessageText": "Hello :) :) :D",
                "TimeStamp": "17 11"
            },
            {
                "UserName": "default_user_2",
                "MessageText": "Hello Arsalan :)",
                "TimeStamp": "17 11"
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


@app.route("/")
def default():
    return redirect("/login")


@app.route("/login", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        # session vars check
        if session["session_id"] == None:
            session["session_id"] = 0
            session["username"] = ""
            print(session["session_id"])
            print(session["username"])
            return render_template("login.html")

        else:
            # check login or not
            if session["session_id"] != 0:
                print(session["session_id"])
                print(session["username"])
                return redirect("/main")
            else:
                print(session["session_id"])
                print(session["username"])
                return render_template("login.html")

    if request.method == "POST":

        if session["session_id"] == None:
            print("session var not present")
            session["session_id"] = 0
            session["username"] = ""
            print(session["session_id"])
            print(session["username"])
            return render_template("login.html")

        else:
            # check login or not
            if session["session_id"] != 0:
                print("session already loggedin")
                print(session["session_id"])
                print(session["username"])
                return redirect("/main")
            else:
                username = request.form.get("username_from_form")
                if username in all_users:
                    print("username already exists")

                    print(session["session_id"])
                    print(session["username"])
                    return render_template("login.html", javascript_alert="Username Already exists! Please choose another one!")
                else:
                    print("creating new username")
                    session["username"] = username
                    session["session_id"] = randint(1, 99)
                    all_users.append(username)
                    print(session["session_id"])
                    print(session["username"])
                    return redirect("/main")


# default page
@app.route("/main", methods=["GET", "POST"])
def main():
    if session["session_id"] == None:
        return redirect("/login")
    else:
        if session["session_id"] == 0:
            return redirect("/login")
        else:
            print(session["session_id"])
            print(session["username"])
            larger = find_larger(all_users, all_channels)
            print(all_users)
            return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger)


@app.route("/channel_create", methods=["POST"])
def channel_create():
    if session["session_id"] == None:
        return redirect("/login")
    else:
        if session["session_id"] == 0:
            return redirect("/login")
        else:
            print(session["session_id"])
            print(session["username"])
            new_channel_to_create = request.form.get("new_channel_from_form")

            if new_channel_to_create in all_channels:
                larger = find_larger(all_users, all_channels)
                return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger, javascript_alert="The Channel already exists!")

            else:

                new_channel_for_all_messages = {
                    "Channel_Name": "", "Channel_Messages": []}

                new_channel_for_all_messages["Channel_Name"] = new_channel_to_create

                # add channel to dict and list
                messages_all_channels.append(new_channel_for_all_messages)
                all_channels.append(new_channel_to_create)

                larger = find_larger(all_users, all_channels)
                print(messages_all_channels)
                print(all_users)
                return render_template("homepage.html", all_users=all_users, all_channels=all_channels, larger=larger)

# channel page
@app.route("/channel", methods=["GET", "POST"])
def channel():
    if session["session_id"] == None:
        return redirect("/login")
    else:
        if session["session_id"] == 0:
            return redirect("/login")
        else:
            print(session["session_id"])
            print(session["username"])
            return render_template("channel.html")



@app.route("/channels/<string:channel>", methods=['GET', 'POST'])
def channels(channel):
    if session["session_id"] == None:
        return redirect("/login")
    else:
        if session["session_id"] == 0:
            return redirect("/login")
        else:
            print(session["session_id"])
            print(session["username"])
        
        #  print(type(channel))
        #   print(channel)
            channel_all_messages = {}
            channel_dict = {}
            # i for i, d in enumerate(listofpeople) if "Jack" in d.keys()
            channel_index = [i for i, d in enumerate(
                messages_all_channels) if channel in d.values()]
        #    print(channel_index)
            #value_index = 0

            channel_dict = (messages_all_channels[channel_index[0]])
        #    print(channel_dict)

            channel_messages_list_of_dict = channel_dict["Channel_Messages"]
            print(channel_messages_list_of_dict)
            # for key1 in channel_dict:
            #     if key1 == "Channel_Messages":
            #         print(key1)
            #         for items in channel_dict[key1]:
            #             print(items)
        #                 channel_all_messages = key2
        #                 channel_all_messages.update
            # print(d)
        # print(channel_dict[messages_index])

            return render_template("channel.html", channel=channel, all_channels=messages_all_channels, channel_all_messages=channel_messages_list_of_dict)


@app.route("/people/<string:person>", methods=['GET', 'POST'])
def people(person):
    if session["session_id"] == None:
        return redirect("/login")
    else:
        if session["session_id"] == 0:
            return redirect("/login")
        else:
            print(session["session_id"])
            print(session["username"])    
            return render_template("people.html", person=person)


@socketio.on("submit vote")
def vote(data):
    username = session["username"]
    selection = data["selection"]
    full_date = datetime.now()
    message_time = str(full_date.hour)+" "+str(full_date.minute)
    channel_name = data["webname"]

    print(data)
    print(channel_name)
    # print(type(data))
    # print(selection)
    # print(message_time)

    emit("announce vote", {"selection": selection,
                           "username": username,
                           "time": message_time,
                           "channel": channel_name}, broadcast=True)
    print("hi")

    for each_channel in messages_all_channels:

        if each_channel["Channel_Name"] == channel_name:

            # check if channel has 100 messages
            print(len(each_channel["Channel_Messages"]))

            print("hlo")

            each_channel["Channel_Messages"].append({
                'UserName': username, 'MessageText': selection, 'TimeStamp': message_time
            })

        # print(each_channel["Channel_Messages"])

    print(messages_all_channels)
    # for each_message in each_channel["Channel_Messages"]:

    #     each_message["UserName"] = username
    #     each_message["MessageText"] = selection
    #     each_message["TimeStamp"] = message_time

    #     new_message = each_message

    # print(new_message)

    # each_channel["Channel_Messages"].append(new_message)

    #    print(each_channel)
    # print(messages_all_channels)


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
