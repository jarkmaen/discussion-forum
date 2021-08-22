CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    username TEXT UNIQUE,
    password TEXT,
    is_admin BOOLEAN DEFAULT FALSE
);

CREATE TABLE topics (
    id SERIAL PRIMARY KEY,
    name TEXT,
    private BOOLEAN DEFAULT FALSE,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE posts (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users,
    title TEXT,
    content TEXT,
    visible BOOLEAN DEFAULT TRUE
);

CREATE TABLE comments (
    id SERIAL PRIMARY KEY,
    post_id INTEGER REFERENCES posts,
    user_id INTEGER REFERENCES users,
    content TEXT
);

CREATE TABLE private_topics (
    id SERIAL PRIMARY KEY,
    topic_id INTEGER REFERENCES topics,
    user_id INTEGER REFERENCES users
);