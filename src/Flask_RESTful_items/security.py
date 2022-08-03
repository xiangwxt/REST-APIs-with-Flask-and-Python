from user import User  # from the user.py import User class

users = [User(1, "bob", "asdf")]

username_mapping = {
    u.username: u for u in users
}  # So we don't need to iterate the users list every time.

userid_mapping = {u.id: u for u in users}


def authenticate(username, password):
    user = username_mapping.get(
        username, None
    )  # get the value of the key, default value is set to None.
    if user and user.password == password:
        return user


def identity(payload):  # unique to flask-jwt, payload is the content of the Jwt token
    user_id = payload["identity"]
    return userid_mapping.get(user_id, None)
