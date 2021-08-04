from db import db

def get_topics():
    sql = "SELECT id, name FROM topics"
    result = db.session.execute(sql)
    return result.fetchall()

def get_topic_info(topic_id):
    sql = "SELECT id, name FROM topics WHERE id=:topic_id"
    result = db.session.execute(sql, {"topic_id":topic_id})
    return result.fetchone()