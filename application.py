import os
from flask import Flask, request, session, render_template, redirect
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
            request.form.get("username_from_form")
            return render_template("homepage.html")            


#default page
@app.route("/main", methods=["GET","POST"])
def main():



    return render_template("homepage.html")




@app.route("/navbar", methods=["GET","POST"])
def navbar():
    return render_template("navbar.html")


@app.route("/test", methods=["GET","POST"])
def test():
    return render_template("test.html")

#default page
@app.route("/js-test", methods=["GET","POST"])
def js():

    return render_template("js-test.html")

