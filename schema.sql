CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    content TEXT
);