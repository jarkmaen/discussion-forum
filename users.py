from db import db
from flask import abort, request, session
from werkzeug.security import check_password_hash, generate_password_hash
import os

def login(username, password):
    sql = "SELECT id, password, is_admin FROM users WHERE username=:username"
    user = db.session.execute(sql, {"username": username}).fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            session["is_admin"] = user.is_admin
            session["csrf_token"] = os.urandom(16).hex()
            return True
        else:
            return False

def logout():
    del session["user_id"]
    del session["username"]
    del session["is_admin"]
    del session["csrf_token"]

def register(username, password):
    hash_value = generate_password_hash(password)
    try:
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username": username, "password": hash_value})
        db.session.commit()
    except:
        return False
    return login(username, password)

def get_user_id(username):
    sql = "SELECT id FROM users WHERE username=:username"
    user_id = db.session.execute(sql, {"username": username}).fetchone()
    if user_id is None:
        return 0
    else:
        return user_id[0]

def has_private_access(topic_id):
    sql = "SELECT id FROM private_topics WHERE topic_id=:topic_id AND user_id=:user_id"
    if db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id()}).fetchone():
        return True
    else:
        return False

def user_id():
    return session.get("user_id", 0)

def is_admin():
    return session.get("is_admin", False)

def check_csrf():
    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
