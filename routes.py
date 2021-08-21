from app import app
from flask import render_template, request, redirect
import comments, posts, topics, users

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        return render_template("index.html", topics=topics.get_topics())
    if request.method == "POST":
        users.check_csrf()
        topic = request.form["topic"]
        if len(topic) < 1 or len(topic) > 50:
            return render_template("error.html", message="Aihe puuttuu tai on liian pitkä")
        if topics.add_topic(topic):
            return render_template("index.html", topics=topics.get_topics())
        else:
            return render_template("error.html", message="Aiheen luomisessa tapahtui virhe")

@app.route("/delete_topic", methods=["POST"])
def delete_topic():
    users.check_csrf()
    topic_id = request.form["topic_id"]
    if topics.delete_topic(topic_id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Keskustelualueen poistamisessa tapahtui virhe")

@app.route("/topic/<int:id>", methods=["GET", "POST"])
def topic(id):
    topic = topics.get_topic_info(id)
    if request.method == "GET":
        return render_template("topic.html", posts=posts.get_posts(id), topic=topic)
    if request.method == "POST":
        users.check_csrf()
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

@app.route("/topic/delete_post", methods=["POST"])
def delete_post():
    users.check_csrf()
    post_id = request.form["post_id"]
    if posts.delete_post(post_id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Keskustelun poistamisessa tapahtui virhe")

@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    post = posts.get_post_info(id)
    if request.method == "GET":
        return render_template("post.html", comments=comments.get_comments(id), post=post)
    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        if len(content) < 1 or len(content) > 2000:
            return render_template("error.html", message="Viesti puuttuu tai on liian pitkä")
        if comments.add_comment(id, content):
            return render_template("post.html", comments=comments.get_comments(id), post=post)
        else:
            return render_template("error.html", message="Kommentin lähettämisessä tapahtui virhe")

@app.route("/post/edit_post", methods=["POST"])
def edit_post():
    users.check_csrf()
    post_id = request.form["post_id"]
    if request.form.get("update"):
        content = request.form["content"]
        if posts.update_post(post_id, content):
            return redirect(request.referrer)
        else:
            return render_template("error.html", message="Viestin muokkauksessa tapahtui virhe")
    elif request.form.get("delete"):
        if posts.delete_post(post_id):
            return redirect(request.referrer)
        else:
            return render_template("error.html", message="Keskustelun poistamisessa tapahtui virhe")

@app.route("/post/edit_comment", methods=["POST"])
def edit_comment():
    users.check_csrf()
    comment_id = request.form["comment_id"]
    if request.form.get("update"):
        comment = request.form["comment"]
        if comments.update_comment(comment_id, comment):
            return redirect(request.referrer)
        else:
            return render_template("error.html", message="Viestin muokkauksessa tapahtui virhe")
    elif request.form.get("delete"):
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
