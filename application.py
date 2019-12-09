import os, json, requests, urllib, random

from cs50 import SQL
from flask import Flask, flash, jsonify, redirect, render_template, request, session, url_for
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required #lookup

# Configure application
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response



# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
# db = SQL("sqlite:///neighbor.db")
db = SQL("postgres://dhxujswbyuzout:16236b614f74a8fa701f8a01751ddbb33ce54d7f22287352af010d43f9305156@ec2-184-72-238-22.compute-1.amazonaws.com:5432/dfv02l7h6iik3c")

# # Make sure API key is set
# if not os.environ.get("API_KEY"):
#     raise RuntimeError("API_KEY not set")


@app.route("/")
def index():
    """Show posts for help in a list and on an interactive map"""

    # posts = db.execute("SELECT * FROM posts WHERE active = :status", status='t')
    posts = db.execute("SELECT * FROM posts;")

    for post in posts:
        datetime = post['post_time']
        # date = datetime.split(" ")[0]


    return render_template("index.html", posts=posts)


@app.route("/about", methods=["GET"])
def about():
    """Show information about website"""

    return render_template("about.html")


@app.route("/messenger", methods=["GET","POST"])
@login_required
def messenger():
    """messenger for people to contact posters"""

    if request.method == "POST":

        ## add message content and info to messeges table
        # Post Info
        message_text=request.form.get("message_text")
        post_id=request.form.get("post_id")
        post_user=request.form.get("post_user")


        # add values to table
        message_id = db.execute("INSERT INTO messages (user_id_1, user_id_2, message, post_id_m) VALUES (:user_id_1, :user_id_2, :message, :post_id_m);",
        user_id_1=post_user, user_id_2=session["user_id"], message=message_text, post_id_m=post_id)

        # end if


    messeges_rec = db.execute("SELECT * FROM messages JOIN users ON messages.user_id_2=users.id WHERE user_id_1 = :user_id_1;",
        user_id_1=session["user_id"])

    messeges_sent = db.execute("SELECT * FROM messages JOIN users ON messages.user_id_1=users.id WHERE user_id_2 = :user_id_2;",
        user_id_2=session["user_id"])

    return render_template("messenger.html", messeges_sent=messeges_sent, messeges_rec=messeges_rec)




@app.route("/post", methods=["GET", "POST"])
@login_required
def post():
    """create a new post"""
    if request.method == "POST":

        # check for valid inputs and alert the user of anything missing
        #TODO

        ## add post information to post table
        # Post Info
        title=request.form.get("inputTitle")
        summary=request.form.get("inputSummary")

        # address inputs
        address1=request.form.get("inputAddress")
        address2=request.form.get("inputAddress2")
        city=request.form.get("inputCity")
        state=request.form.get("inputState")
        zipcode=request.form.get("inputZip")

        # additional Info
        minHelp=request.form.get("inputMinHelp")
        maxHelp=request.form.get("inputMaxHelp")
        hoursEst=request.form.get("inputHours")
        workType=request.form.get("inputWork")

        # concatenat address and geocode into LAT,LONG coordintes
        AddressFull = address1 + address2 + ", " + city + ", " + state
        # AddressFull = "1600+Amphitheatre+Parkway,+Mountain+View,+CA"

        # url variable store url
        url = 'https://maps.googleapis.com/maps/api/geocode/json?'
        api_key="AIzaSyAK2psyrrWMo41mcGCnga6ITxShJqGJLoc"

        fullUrl = url + 'address=' + AddressFull.replace(" ", "+") + '&key=' + api_key

        # request the geolocation
        geolocation = json.load(urllib.request.urlopen(fullUrl))

        geo_lat = geolocation['results'][0]['geometry']['location']['lat']
        geo_lng = geolocation['results'][0]['geometry']['location']['lng']

        # randomize the displayed location for privacy
        rand_geo_lat = float(geo_lat) + random.choice([-1,1])*random.randrange(150,300)*0.00001
        rand_geo_lng = float(geo_lng) + random.choice([-1,1])*random.randrange(150,300)*0.00001


        # add values to table
        post_id = db.execute("INSERT INTO posts (post_user, title, address, summary, work_type, est_hour, min_help, max_help, geo_lat, geo_lng, rand_geo_lat, rand_geo_lng) VALUES (:post_user, :title, :address, :summary, :work_type, :est_hour, :min_help, :max_help, :geo_lat, :geo_lng, :rand_geo_lat, :rand_geo_lng);",
            post_user=session["user_id"], title=title, address=AddressFull, summary=summary, work_type=workType, est_hour=hoursEst, min_help=minHelp, max_help=maxHelp, geo_lat=geo_lat, geo_lng=geo_lng, rand_geo_lat=rand_geo_lat, rand_geo_lng=rand_geo_lng)

        # Redirect user to viewpost page along with the post_id
        return redirect(url_for(".viewpost", post_id = post_id))

    else:
        return render_template("create_post.html")




@app.route("/viewpost", methods=["GET", "POST"])
def viewpost():
    """Show information about website"""

    if request.method == "POST":
        post_id = request.form.get("post_id")

    else:
        post_id = request.args['post_id']  # counterpart for url_for()


    # Query database for post info
    rows = db.execute("SELECT * FROM posts WHERE post_id = :post_id;",
                      post_id=post_id)

    if session.get("user_id") is None:
        user_status = "none"
    else:
        user_status = session["user_id"]

    return render_template("viewpost.html", rows=rows, user_status=user_status)


@app.route("/profile", methods=["GET"])
@login_required
def profile():
    """Show information about website"""

    ##DEBUGGING
    return redirect(url_for(".viewpost", post_id = 4))

    # return render_template("profile.html")



@app.route("/login", methods=["GET", "POST"])
def login():
    """Log user in"""

    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username;",
                          username=request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")


@app.route("/register", methods=["GET", "POST"])
def register():
    """Register user"""
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Ensure confirm password was submitted
        elif not request.form.get("confirmpassword"):
            return apology("must confrim your password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username;",
                          username=request.form.get("username"))

        if len(rows) == 1:
            return apology("username already taken")

        if request.form.get("password") != request.form.get("confirmpassword"):
            return apology("passwords do not match")

        # inputs are valid, so now register the user
        # hash the users input password to be stored in the database
        passwordhash = generate_password_hash(request.form.get("password"))

        db.execute("INSERT INTO users (username, hash) VALUES (:username, :hash);",
                    username=request.form.get("username"), hash=passwordhash)


        #log the new user in
        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = :username;",
                          username=request.form.get("username"))

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    else:
        return render_template("register.html")


def errorhandler(e):
    """Handle error"""
    if not isinstance(e, HTTPException):
        e = InternalServerError()
    return apology(e.name, e.code)


# Listen for errors
for code in default_exceptions:
    app.errorhandler(code)(errorhandler)
