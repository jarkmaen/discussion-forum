from app import app
from flask import render_template, request, redirect
import comments, posts, topics, users

@app.route("/")
def index():
    list = topics.get_topics()
    return render_template("index.html", topics=list)

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    topic = topics.get_topic_info(id)
    if request.method == "GET":
        return render_template("topic.html", posts=posts.get_posts(id), topic=topic)
    if request.method == "POST":
        title = request.form["title"]
        content = request.form["content"]
        if len(title) < 1 or len(title) > 500:
            return render_template("error.html", message="Otsikko puuttuu tai on liian pitkä")
        if len(content) < 1 or len(content) > 2000:
            return render_template("error.html", message="Viesti puuttuu tai on liian pitkä")
        if posts.add_post(id, title, content):
            return render_template("topic.html", posts=posts.get_posts(id), topic=topic)
        else:
            return render_template("error.html", message="Keskustelun luomisessa tapahtui virhe")

@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    post = posts.get_post_info(id)
    if request.method == "GET":
        return render_template("post.html", comments=comments.get_comments(id), post=post)
    if request.method == "POST":
        content = request.form["content"]
        if len(content) < 1 or len(content) > 2000:
            return render_template("error.html", message="Viesti puuttuu tai on liian pitkä")
        if comments.add_comment(id, content):
            return render_template("post.html", comments=comments.get_comments(id), post=post)
        else:
            return render_template("error.html", message="Kommentin lähettämisessä tapahtui virhe")

@app.route("/post/delete_comment", methods=["POST"])
def delete_comment():
    comment_id = request.form["comment_id"]
    if comments.delete_comment(comment_id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Viestin poistamisessa tapahtui virhe")

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
            return render_template("error.html", message="Väärä tunnus tai salasana")

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
        if len(username) < 1 or len(username) > 16:
            return render_template("error.html", message="Tunnuksen tulee sisältää 1-16 merkkiä")
        if password == "":
            return render_template("error.html", message="Salasanakenttä on tyhjä")
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinnissä tapahtui virhe")
