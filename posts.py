from db import db
import users

def get_posts(topic_id):
    sql = "SELECT id, title FROM posts WHERE topic_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_post_info(post_id):
    sql = "SELECT P.id, P.topic_id, U.username, P.title, P.content FROM posts P INNER JOIN users U ON P.user_id=U.id WHERE P.id=:post_id"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()

def add_post(topic_id, title, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO posts (topic_id, user_id, title, content) VALUES (:topic_id, :user_id, :title, :content)"
    db.session.execute(sql, {"topic_id":topic_id, "user_id":user_id, "title":title, "content":content})
    db.session.commit()
    return True