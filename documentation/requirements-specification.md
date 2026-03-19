# Requirements specification

The objective of this project is to build a simple discussion forum web application where users can participate in conversations within predefined topics. The application will support both public and private discussion areas, user authentication and administrative tools for forum management.

## Basic functionality

### User

- Users can register a new account.
- Users can log in and log out.
- Users can browse different topics.
- Users can browse posts within a topic.
- Users can create new posts in public topics.
- Users can create new posts in private topics, if they have been invited to that specific topic by an admin.
- Users can post comments in existing posts.
- Users can edit or delete their own posts and comments.
- Users can search for posts by title.
- Users can view their account statistics and comment history.
    - Statistics include the number of posts created and comments posted.

### Admin

- Admins can add and remove topics.
- Admins can remove posts and comments created by other users.
- Admins can create private topics and invite users to them by their username.
