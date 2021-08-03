from db import db

def get_posts(topic_id):
    sql = "SELECT id, title FROM posts WHERE topic_id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchall()

def get_post_info(post_id):
    sql = "SELECT U.username, P.title, P.content FROM posts P INNER JOIN users U ON P.user_id=U.id WHERE P.id=:post_id;"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchone()