from db import db
import users

def get_comments(post_id):
    sql = "SELECT U.username, C.content FROM comments C INNER JOIN users U ON C.user_id=U.id WHERE C.post_id=:post_id;"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchall()

def add_comment(post_id, content):
    user_id = users.user_id()
    if user_id == 0:
        return False
    sql = "INSERT INTO comments (post_id, user_id, content) VALUES (:post_id, :user_id, :content)"
    db.session.execute(sql, {"post_id":post_id, "user_id":user_id, "content":content})
    db.session.commit()
    return True