from db import db
import users

def get_topics():
    sql = "SELECT id, name FROM topics WHERE visible=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def get_topic_info(topic_id):
    sql = "SELECT id, name, visible FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()

def add_topic(topic):
    if not users.is_admin:
        return False
    sql = "INSERT INTO topics (name) VALUES (:topic)"
    db.session.execute(sql, {"topic":topic})
    db.session.commit()
    return True

def delete_topic(topic_id):
    if not users.is_admin:
        return False
    sql = "UPDATE topics SET visible=FALSE WHERE id=:topic_id; " \
          "UPDATE posts SET visible=FALSE WHERE topic_id=:topic_id; " \
          "DELETE FROM comments C USING posts P WHERE C.post_id=P.id AND P.topic_id=:topic_id"
    db.session.execute(sql, {"topic_id":topic_id})
    db.session.commit()
    return True