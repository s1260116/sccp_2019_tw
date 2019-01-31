import MyTwtr_DB as DB
from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    if session.get("username") is not None:
        return render_template("index.html", username=session["username"])
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if DB.login_user(username) == None:
            DB.add_user(username, password)
            userData = DB.login_user(username)
            session["username"] = username
            session["user_id"] = userData[0]
            return render_template("index.html", username=session["username"])
    return render_template("create.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    error = None
    if session.get("username") is not None:
        return render_template("index.html", username=session["username"])
    if request.method == "POST":
        userData = DB.login_user(request.form["username"])
        pword = request.form["password"]
        ec_pass = DB.hashlib.sha256(pword.encode('utf-8')).hexdigest()
        if userData[2] == ec_pass:
            session["username"] = userData[1]
            session["user_id"] = userData[0]
            return render_template("index.html", username=session["username"])
        else:
            error = "Invalid username/password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.pop("username", None)
    session.pop("user_id", None)
    return render_template("index.html")

@app.route("/tweet", methods=["POST", "GET"])
def tweet():
    if request.method == "POST":
        text = request.form["text"]
        DB.post_tweet(session["user_id"], text)
    tweets = DB.get_tweets()
    return render_template("timeline.html", tweets=tweets)

app.secret_key = 'ri2@#R@38{ERF:L{$:L87y'

if __name__ == "__main__":
    app.run(debug = True)
    DB.connection.close()
