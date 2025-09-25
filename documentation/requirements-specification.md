# Requirements specification

This document defines the minimum required features for the discussion forum application. The goal is to provide a platform where registered users can participate in conversations. The application will have both public and private discussion areas (called topics), user authentication, and tools for administrators to manage the forum.

## Basic functionality

### User

- Users can register a new account.
- Users can log in and log out.
- Users can browse different topics.
- Users can browse posts within a topic.
- Users can create new posts in public topics.
- Users can create new posts in private topics only if they have been invited.
- Users can post comments in existing posts.
- Users can edit or delete their own comments and posts.
- Users can search for topics by title.
- Users can view their own statistics and comment history.
  - Statistics include the number of comments posted and posts created.

### Admin

- Admins can add and remove topics.
- Admins can delete posts and comments created by other users.
- Admins can create private topics and invite users by username.