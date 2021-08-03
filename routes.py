from app import app
from flask import render_template, request, redirect
import messages, posts, topics, users

@app.route("/")
def index():
    list = topics.get_topics()
    return render_template("index.html", topics=list)

@app.route("/topic/<int:id>")
def topic(id):
    list = posts.get_posts(id)
    topic = topics.get_topic_info(id)
    return render_template("topic.html", posts=list, topic=topic[0])

@app.route("/post/<int:id>")
def post(id):
    list = messages.get_messages(id)
    post = posts.get_post_info(id)
    return render_template("post.html", messages=list, creator=post[0], title=post[1], content=post[2])

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return None

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return None
