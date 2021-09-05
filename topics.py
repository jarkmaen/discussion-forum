from db import db
import users

def get_topics():
    sql = "SELECT id, name FROM topics WHERE visible=TRUE AND private=FALSE"
    return db.session.execute(sql).fetchall()

def get_private_topics():
    sql = "SELECT DISTINCT T.id, T.name FROM topics T INNER JOIN private_topics P " \
          "ON T.id=P.topic_id WHERE T.visible=TRUE AND T.private=TRUE AND P.user_id=:user_id"
    return db.session.execute(sql, {"user_id": users.user_id()}).fetchall()

def get_topic_info(topic_id):
    sql = "SELECT id, name, visible, private FROM topics WHERE id=:topic_id"
    return db.session.execute(sql, {"topic_id": topic_id}).fetchone()

def add_topic(topic, private):
    if not users.is_admin:
        return False
    sql = "INSERT INTO topics (name, private) VALUES (:topic, :private) RETURNING id"
    result = db.session.execute(sql, {"topic": topic, "private": private})
    db.session.commit()
    if private:
        add_user(result.fetchone()[0], users.user_id())
    return True

def add_user(topic_id, user_id):
    sql = "INSERT INTO private_topics (topic_id, user_id) VALUES (:topic_id, :user_id)"
    db.session.execute(sql, {"topic_id": topic_id, "user_id": user_id})
    db.session.commit()

def delete_topic(topic_id):
    if not users.is_admin:
        return False
    sql = "UPDATE topics SET visible=FALSE WHERE id=:topic_id; " \
          "UPDATE posts SET visible=FALSE WHERE topic_id=:topic_id; " \
          "DELETE FROM comments C USING posts P WHERE C.post_id=P.id AND P.topic_id=:topic_id"
    db.session.execute(sql, {"topic_id": topic_id})
    db.session.commit()
    return True
