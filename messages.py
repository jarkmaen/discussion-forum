from db import db

def get_messages(post_id):
    sql = "SELECT U.username, C.content FROM comments C INNER JOIN users U ON C.user_id=U.id WHERE C.post_id=:post_id;"
    result = db.session.execute(sql, {"post_id":post_id})
    return result.fetchall()