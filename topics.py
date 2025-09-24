from db import db
from sqlalchemy import text
import users


def add_topic(private, title):
    if not users.is_admin:
        return False

    sql = text("INSERT INTO topics (private, title) VALUES (:private, :title) RETURNING id")
    topic_id = db.session.execute(sql, {"private": private, "title": title}).fetchone()[0]
    db.session.commit()

    if private:
        add_user_to_private_topic(topic_id, users.get_current_user_id())

    return True


def add_user_to_private_topic(topic_id, user_id):
    sql = text("INSERT INTO private_topics (topic_id, user_id) VALUES (:topic_id, :user_id)")
    db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id})
    db.session.commit()


def delete_topic(topic_id):
    if not users.is_admin:
        return False

    sql = text("UPDATE topics SET visible=FALSE WHERE id=:topic_id")
    db.session.execute(sql, {"topic_id": topic_id})

    sql = text("UPDATE posts SET visible=FALSE WHERE topic_id=:topic_id")
    db.session.execute(sql, {"topic_id": topic_id})

    sql = text("DELETE FROM comments WHERE post_id IN (SELECT id FROM posts WHERE topic_id=:topic_id)")
    db.session.execute(sql, {"topic_id": topic_id})

    db.session.commit()

    return True


def get_private_topics():
    sql = text(
        "SELECT DISTINCT T.id, T.title FROM topics T INNER JOIN private_topics P "
        "ON T.id=P.topic_id WHERE T.visible=TRUE AND T.private=TRUE AND P.user_id=:user_id"
    )

    return db.session.execute(sql, {"user_id": users.get_current_user_id()}).fetchall()


def get_topic(topic_id):
    sql = text("SELECT id, title, visible, private FROM topics WHERE id=:topic_id")
    return db.session.execute(sql, {"topic_id": topic_id}).fetchone()


def get_topics():
    sql = text("SELECT id, title FROM topics WHERE visible=TRUE AND private=FALSE")
    return db.session.execute(sql).fetchall()
