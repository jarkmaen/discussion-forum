from app import app
from flask import render_template, request, redirect
import comments, posts, topics, users

@app.route("/", methods=["GET", "POST"])
def index():
    topics_list = topics.get_topics()
    private_topics = topics.get_private_topics()
    if request.method == "GET":
        return render_template("index.html", topics=topics_list, private_topics=private_topics)
    if request.method == "POST":
        users.check_csrf()
        topic = request.form["topic"]
        private = request.form["private"]
        if len(topic) < 1 or len(topic) > 50:
            error = "Aihe puuttuu tai on liian pitkä (maksimissaan 50 merkkiä)"
            return render_template("index.html", topics=topics_list, private_topics=private_topics, error=error)
        if topics.add_topic(topic, private):
            return render_template("index.html", topics=topics.get_topics(), private_topics=topics.get_private_topics())
        else:
            error = "Aiheen luomisessa tapahtui virhe"
            return render_template("index.html", topics=topics_list, private_topics=private_topics, error=error)

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
    posts_list = posts.get_posts(id)
    topic = topics.get_topic_info(id)
    has_access = False
    if topic.private and users.has_private_access(id):
        has_access = True
    if request.method == "GET":
        return render_template("topic.html", posts=posts.get_posts(id), topic=topic, has_access=has_access)
    if request.method == "POST":
        users.check_csrf()
        title = request.form["title"]
        content = request.form["content"]
        if len(title) < 1 or len(title) > 100:
            error = "Otsikko puuttuu tai on liian pitkä (maksimissaan 100 merkkiä)"
            return render_template("topic.html", posts=posts_list, topic=topic, has_access=has_access, error=error)
        if len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
            return render_template("topic.html", posts=posts_list, topic=topic, has_access=has_access, error=error)
        if posts.add_post(id, title, content):
            return render_template("topic.html", posts=posts.get_posts(id), topic=topics.get_topic_info(id), has_access=has_access)
        else:
            error = "Keskustelun luomisessa tapahtui virhe"
            return render_template("topic.html", posts=posts_list, topic=topic, has_access=has_access, error=error)

@app.route("/topic/delete_post", methods=["POST"])
def delete_post():
    users.check_csrf()
    post_id = request.form["post_id"]
    if posts.delete_post(post_id):
        return redirect(request.referrer)
    else:
        return render_template("error.html", message="Keskustelun poistamisessa tapahtui virhe")

@app.route("/topic/add_member", methods=["POST"])
def add_member():
    users.check_csrf()
    username = request.form["username"]
    topic_id = request.form["topic_id"]
    user_id = users.get_user_id(username)
    posts_list = posts.get_posts(topic_id)
    topic = topics.get_topic_info(topic_id)
    if user_id == 0:
        error = "Käyttäjää ei löytynyt (huom. tunnukset ovat merkkikokoriippuvaisia)"
        return render_template("topic.html", posts=posts_list, topic=topic, has_access=True, error=error)
    if topics.add_user(topic_id, user_id):
        return render_template("topic.html", posts=posts.get_posts(topic_id), topic=topics.get_topic_info(topic_id), has_access=True)
    else:
        error = "Jäsenen lisäämisessä tapahtui virhe"
        return render_template("topic.html", posts=posts_list, topic=topic, has_access=True, error=error)

@app.route("/post/<int:id>", methods=["GET", "POST"])
def post(id):
    comments_list = comments.get_comments(id)
    post = posts.get_post_info(id)
    has_access = False
    if post.private and users.has_private_access(post.topic_id):
        has_access = True
    if request.method == "GET":
        return render_template("post.html", comments=comments.get_comments(id), post=post, has_access=has_access)
    if request.method == "POST":
        users.check_csrf()
        content = request.form["content"]
        if len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
            return render_template("post.html", comments=comments_list, post=post, has_access=has_access, error=error)
        if comments.add_comment(id, content):
            return render_template("post.html", comments=comments.get_comments(id), post=posts.get_post_info(id), has_access=has_access)
        else:
            error = "Kommentin lähettämisessä tapahtui virhe"
            return render_template("post.html", comments=comments_list, post=post, has_access=has_access, error=error)

@app.route("/post/edit_post", methods=["POST"])
def edit_post():
    users.check_csrf()
    post_id = request.form["post_id"]
    comments_list = comments.get_comments(post_id)
    post = posts.get_post_info(post_id)
    if request.form.get("update"):
        content = request.form["content"]
        if len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
            return render_template("post.html", comments=comments_list, post=post, error=error)
        if posts.update_post(post_id, content):
            return render_template("post.html", comments=comments.get_comments(post_id), post=posts.get_post_info(post_id))
        else:
            error = "Viestin muokkauksessa tapahtui virhe"
            return render_template("post.html", comments=comments_list, post=post, error=error)
    elif request.form.get("delete"):
        if posts.delete_post(post_id):
            return render_template("post.html", comments=comments.get_comments(post_id), post=posts.get_post_info(post_id))
        else:
            error = "Keskustelun poistamisessa tapahtui virhe"
            return render_template("post.html", comments=comments_list, post=post, error=error)

@app.route("/post/edit_comment", methods=["POST"])
def edit_comment():
    users.check_csrf()
    post_id = request.form["post_id"]
    comment_id = request.form["comment_id"]
    comments_list = comments.get_comments(post_id)
    post = posts.get_post_info(post_id)
    if request.form.get("update"):
        comment = request.form["comment"]
        if len(comment) < 1 or len(comment) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
            return render_template("post.html", comments=comments_list, post=post, error=error)
        if comments.update_comment(comment_id, comment):
            return render_template("post.html", comments=comments.get_comments(post_id), post=posts.get_post_info(post_id))
        else:
            error = "Viestin muokkauksessa tapahtui virhe"
            return render_template("post.html", comments=comments_list, post=post, error=error)
    elif request.form.get("delete"):
        if comments.delete_comment(comment_id):
            return render_template("post.html", comments=comments.get_comments(post_id), post=posts.get_post_info(post_id))
        else:
            error = "Viestin poistamisessa tapahtui virhe"
            return render_template("post.html", comments=comments_list, post=post, error=error)

@app.route("/profile/<int:id>")
def profile(id):
    post_count = posts.get_user_post_count(id)
    comment_count = comments.get_user_comment_count(id)
    user_comments = comments.get_user_comment_history(id)
    return render_template("profile.html", user_id=id, post_count=post_count[0], comment_count=comment_count[0], user_comments=user_comments)

@app.route("/search", methods=["POST"])
def search():
    word = request.form["word"]
    results = posts.search_posts(word)
    return render_template("search.html", word=word, count=len(results), results=results)

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
            return render_template("login.html", error="Väärä tunnus tai salasana")

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
            return render_template("register.html", error="Tunnuksen tulee sisältää 1-16 merkkiä")
        if password == "":
            return render_template("register.html", error="Salasanakenttä on tyhjä")
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("register.html", error="Rekisteröinnissä tapahtui virhe")