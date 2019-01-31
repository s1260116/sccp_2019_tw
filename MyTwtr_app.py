import MyTwtr_DB as DB
from flask import *

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/create", methods=["POST", "GET"])
def create():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if DB.login_user(username) == None:
            DB.add_user(username, password)
            session["username"] = username
            return render_template("index.html", username=session["username"])
    return render_template("create.html")

@app.route("/tweet", methods=["POST", "GET"])
def tweet():
    if request.method == "POST":
        text = request.form["text"]
        DB.post_tweet(0, text)
    tweets = DB.get_tweets()
    return render_template("timeline.html", tweets=tweets)

app.secret_key = 'ri2@#R@38{ERF:L{$:L87y'

if __name__ == "__main__":
    app.run(debug = True)
    DB.connection.close()
