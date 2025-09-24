from db import db
from sqlalchemy import text
import users


def add_post(content, title, topic_id):
    user_id = users.get_current_user_id()

    if user_id == 0:
        return False

    sql = text("INSERT INTO posts (content, title, topic_id, user_id) VALUES (:content, :title, :topic_id, :user_id)")
    db.session.execute(sql, {"content": content, "title": title, "topic_id": topic_id, "user_id": user_id})
    db.session.commit()

    return True


def delete_post(post_id):
    user_id = users.get_current_user_id()

    if not users.is_admin:
        if user_id == 0 or user_id != get_original_poster(post_id)[0]:
            return False

    sql = text("UPDATE posts SET visible=FALSE WHERE id=:post_id")
    db.session.execute(sql, {"post_id": post_id})

    sql = text("DELETE FROM comments WHERE post_id IN (SELECT id FROM posts WHERE visible=FALSE)")
    db.session.execute(sql)

    db.session.commit()

    return True


def find_posts_by_title(title):
    sql = text(
        "SELECT P.id, P.title, T.private FROM posts P INNER JOIN topics T ON P.topic_id=T.id "
        "WHERE P.title ILIKE :title AND T.private=FALSE AND P.visible=TRUE"
    )

    return db.session.execute(sql, {"title": "%" + title + "%"}).fetchall()


def get_original_poster(post_id):
    sql = text("SELECT user_id FROM posts WHERE id=:post_id")
    return db.session.execute(sql, {"post_id": post_id}).fetchone()


def get_post(post_id):
    sql = text(
        "SELECT P.id, P.topic_id, P.user_id, U.username, P.title, P.content, T.private, P.visible FROM posts P "
        "INNER JOIN users U ON P.user_id=U.id INNER JOIN topics T ON P.topic_id=T.id "
        "WHERE P.id=:post_id"
    )

    return db.session.execute(sql, {"post_id": post_id}).fetchone()


def get_posts(topic_id):
    sql = text("SELECT id, user_id, title FROM posts WHERE topic_id=:topic_id AND visible=TRUE")
    return db.session.execute(sql, {"topic_id": topic_id}).fetchall()


def get_user_posts_count(user_id):
    sql = text("SELECT COUNT(*) FROM posts WHERE user_id=:user_id AND visible=TRUE")
    return db.session.execute(sql, {"user_id": user_id}).fetchone()


def update_post(content, post_id):
    user_id = users.get_current_user_id()

    if user_id == 0 or user_id != get_original_poster(post_id)[0]:
        return False

    sql = text("UPDATE posts SET content=:content WHERE id=:post_id")
    db.session.execute(sql, {"post_id": post_id, "content": content})
    db.session.commit()

    return True
