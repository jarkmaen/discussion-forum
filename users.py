from db import db
from flask import abort, request, session
from sqlalchemy import text
from werkzeug.security import check_password_hash, generate_password_hash
import os


def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)


def find_user_id_by_username(username):
    sql = text("SELECT id FROM users WHERE username=:username")
    user_id = db.session.execute(sql, {"username": username}).fetchone()

    if user_id is None:
        return 0
    else:
        return user_id[0]


def get_current_user_id():
    return session.get("user_id", 0)


def has_private_access(topic_id):
    sql = text("SELECT id FROM private_topics WHERE topic_id=:topic_id AND user_id=:user_id")

    if db.session.execute(sql, {"topic_id": topic_id, "user_id": get_current_user_id()}).fetchone():
        return True
    else:
        return False


def is_admin():
    return session.get("is_admin", False)


def login(password, username):
    sql = text("SELECT id, password, is_admin FROM users WHERE username=:username")
    user = db.session.execute(sql, {"username": username}).fetchone()

    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["csrf_token"] = os.urandom(16).hex()
            session["is_admin"] = user.is_admin
            session["user_id"] = user.id
            session["username"] = username

            return True
        else:
            return False


def logout():
    del session["csrf_token"]
    del session["is_admin"]
    del session["user_id"]
    del session["username"]


def register(password, username):
    hash_value = generate_password_hash(password)

    try:
        sql = text("INSERT INTO users (password, username) VALUES (:password, :username)")
        db.session.execute(sql, {"password": hash_value, "username": username})
        db.session.commit()
    except:
        return False

    return login(password, username)
