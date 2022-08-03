from user import User  # from the user.py import User class


def authenticate(username, password):
    user = User.find_by_username(username)
    if user and user.password == password:
        return user


def identity(payload):  # unique to flask-jwt, payload is the content of the Jwt token
    user_id = payload["identity"]
    return User.find_by_id(user_id)
