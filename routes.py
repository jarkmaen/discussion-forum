from app import app
from flask import redirect, render_template, request
import comments, posts, topics, users


@app.route("/", methods=["GET", "POST"])
def index():
    topics_list = topics.get_topics()
    private_topics_list = topics.get_private_topics()

    if request.method == "GET":
        return render_template("index.html", private_topics=private_topics_list, topics=topics_list)

    if request.method == "POST":
        users.check_csrf()

        error = None
        private = request.form["private"]
        title = request.form["title"]

        if len(title) < 1 or len(title) > 50:
            error = "Aihe puuttuu tai on liian pitkä (maksimissaan 50 merkkiä)"
        elif topics.add_topic(private == "true", title):
            return render_template("index.html", private_topics=topics.get_private_topics(), topics=topics.get_topics())
        else:
            error = "Aiheen luomisessa tapahtui virhe"

        return render_template("index.html", error=error, private_topics=private_topics_list, topics=topics_list)


@app.route("/delete_topic", methods=["POST"])
def delete_topic():
    users.check_csrf()

    topic_id = request.form["topic_id"]

    if topics.delete_topic(topic_id):
        return redirect(request.referrer)
    else:
        error = "Keskustelualueen poistamisessa tapahtui virhe"
        return render_template(
            "index.html", error=error, private_topics=topics.get_private_topics(), topics=topics.get_topics()
        )


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    if request.method == "POST":
        password = request.form["password"]
        username = request.form["username"]

        if users.login(password, username):
            return redirect("/")
        else:
            return render_template("login.html", error="Väärä tunnus tai salasana")


@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")


@app.route("/post/<int:post_id>", methods=["GET", "POST"])
def post(post_id):
    comments_list = comments.get_comments(post_id)

    post = posts.get_post(post_id)
    access = users.has_private_access(post.topic_id)

    if request.method == "GET":
        return render_template("post.html", access=access, comments=comments_list, post=post)

    if request.method == "POST":
        users.check_csrf()

        content = request.form["content"]

        if len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
        elif comments.add_comment(content, post_id):
            return render_template(
                "post.html", access=access, comments=comments.get_comments(post_id), post=posts.get_post(post_id)
            )
        else:
            error = "Kommentin lähettämisessä tapahtui virhe"

    return render_template("post.html", access=access, comments=comments_list, error=error, post=post)


@app.route("/post/edit_comment", methods=["POST"])
def edit_comment():
    users.check_csrf()

    error = None

    post_id = request.form["post_id"]
    comment_id = request.form["comment_id"]
    comments_list = comments.get_comments(post_id)
    post = posts.get_post(post_id)
    access = users.has_private_access(post.topic_id)

    if request.form.get("update"):
        content = request.form["content"]

        if len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
        elif comments.update_comment(comment_id, content):
            return render_template(
                "post.html", access=access, comments=comments.get_comments(post_id), post=posts.get_post(post_id)
            )
        else:
            error = "Viestin muokkauksessa tapahtui virhe"
    elif request.form.get("delete"):
        if comments.delete_comment(comment_id):
            return render_template(
                "post.html", access=access, comments=comments.get_comments(post_id), post=posts.get_post(post_id)
            )
        else:
            error = "Viestin poistamisessa tapahtui virhe"

    return render_template("post.html", access=access, comments=comments_list, error=error, post=post)


@app.route("/post/edit_post", methods=["POST"])
def edit_post():
    users.check_csrf()

    error = None

    post_id = request.form["post_id"]
    comments_list = comments.get_comments(post_id)
    post = posts.get_post(post_id)
    access = users.has_private_access(post.topic_id)

    if request.form.get("update"):
        content = request.form["content"]

        if len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
        elif posts.update_post(content, post_id):
            return render_template(
                "post.html", access=access, comments=comments.get_comments(post_id), post=posts.get_post(post_id)
            )
        else:
            error = "Viestin muokkauksessa tapahtui virhe"
    elif request.form.get("delete"):
        if posts.delete_post(post_id):
            return render_template(
                "post.html", access=access, comments=comments.get_comments(post_id), post=posts.get_post(post_id)
            )
        else:
            error = "Keskustelun poistamisessa tapahtui virhe"

    return render_template("post.html", access=access, comments=comments_list, error=error, post=post)


@app.route("/profile/<int:user_id>")
def profile(user_id):
    comments_count = comments.get_user_comments_count(user_id)
    posts_count = posts.get_user_posts_count(user_id)
    user_comments = comments.get_user_comments_history(user_id)

    return render_template(
        "profile.html",
        comments_count=comments_count[0],
        posts_count=posts_count[0],
        user_comments=user_comments,
        user_id=user_id,
    )


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    error = None
    password = request.form["password"]
    username = request.form["username"]

    if len(username) < 1 or len(username) > 16:
        error = "Tunnuksen tulee sisältää 1-16 merkkiä"
    elif password == "":
        error = "Salasanakenttä on tyhjä"
    elif not users.register(password, username):
        error = "Rekisteröinnissä tapahtui virhe"

    if error:
        return render_template("register.html", error=error)
    else:
        return redirect("/")


@app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    results = posts.find_posts_by_title(keyword)
    return render_template("search.html", count=len(results), keyword=keyword, results=results)


@app.route("/topic/<int:topic_id>", methods=["GET", "POST"])
def topic(topic_id):
    access = users.has_private_access(topic_id)
    posts_list = posts.get_posts(topic_id)
    topic = topics.get_topic(topic_id)

    if request.method == "GET":
        return render_template("topic.html", access=access, posts=posts_list, topic=topic)

    if request.method == "POST":
        users.check_csrf()

        content = request.form["content"]
        error = None
        title = request.form["title"]

        if len(title) < 1 or len(title) > 100:
            error = "Otsikko puuttuu tai on liian pitkä (maksimissaan 100 merkkiä)"
        elif len(content) < 1 or len(content) > 2000:
            error = "Viesti puuttuu tai on liian pitkä (maksimissaan 2000 merkkiä)"
        elif posts.add_post(content, title, topic_id):
            return render_template(
                "topic.html", access=access, posts=posts.get_posts(topic_id), topic=topics.get_topic(topic_id)
            )
        else:
            error = "Keskustelun luomisessa tapahtui virhe"

        return render_template("topic.html", access=access, error=error, posts=posts_list, topic=topic)


@app.route("/topic/add_user", methods=["POST"])
def add_user():
    users.check_csrf()

    error = None

    username = request.form["username"]
    user_id = users.find_user_id_by_username(username)

    topic_id = request.form["topic_id"]
    posts_list = posts.get_posts(topic_id)
    topic = topics.get_topic(topic_id)

    if user_id == 0:
        error = "Käyttäjää ei löytynyt (huom. tunnukset ovat merkkikokoriippuvaisia)"
    else:
        topics.add_user_to_private_topic(topic_id, user_id)

    return render_template("topic.html", access=True, error=error, posts=posts_list, topic=topic)


@app.route("/topic/delete_post", methods=["POST"])
def delete_post():
    users.check_csrf()

    if posts.delete_post(request.form["post_id"]):
        return redirect(request.referrer)
    else:
        access = users.has_private_access(topic_id)
        error = "Keskustelun poistamisessa tapahtui virhe"
        posts_list = posts.get_posts(topic_id)

        topic_id = request.form["topic_id"]
        topic = topics.get_topic(topic_id)

        return render_template("topic.html", access=access, error=error, posts=posts_list, topic=topic)
