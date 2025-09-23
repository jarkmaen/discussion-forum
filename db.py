from app import app
from flask_sqlalchemy import SQLAlchemy
from os import getenv
from sqlalchemy import inspect, text

uri = getenv("DATABASE_URI")

app.config["SQLALCHEMY_DATABASE_URI"] = uri
# app.config["SQLALCHEMY_ECHO"] = True

db = SQLAlchemy(app)

with app.app_context():
    # Initialize tables if needed
    inspector = inspect(db.engine)

    if not inspector.has_table("users"):
        with open("schema.sql", "r") as f:
            schema_sql = f.read()

        for sql in schema_sql.split(";"):
            statement = sql.strip()

            if statement:
                db.session.execute(text(statement))

    db.session.commit()

    # Ensure admin user exists
    sql = text("SELECT id FROM users WHERE username = :username")
    admin = db.session.execute(sql, {"username": "admin"}).fetchone()

    # Hash for password "admin". Generated with werkzeug.security.generate_password_hash
    admin_password = "scrypt:32768:8:1$QoKhaEQ9g3YYP39X$220e703ee37255084fb1117c2b575792a78e203f99c2f4a086c49950c4f0ac8f43e0d9fc5e17740c40061e4ed78f488949cb7e2b4a9bce88f4a8d20f482f0b26"

    if not admin:
        sql = text("INSERT INTO users (username, password, is_admin) VALUES (:username, :password, TRUE)")
        db.session.execute(sql, {"username": "admin", "password": admin_password})
        db.session.commit()
