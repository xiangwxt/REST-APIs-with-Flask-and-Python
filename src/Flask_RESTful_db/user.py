import sqlite3
from flask_restful import Resource, reqparse

# to look up users already stored in the data base
class User:
    def __init__(self, _id, username, password):
        self.id = _id  # id is a python keyword
        self.username = username
        self.password = password

    @classmethod  # without hard coding the class name there
    def find_by_username(cls, username):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE username=?"
        result = cursor.execute(
            query, (username,)
        )  # user comma to indicate that this is a tuple, not a bracket that prioritize the execution of variables inside it.
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user

    @classmethod
    def find_by_id(cls, _id):
        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()

        query = "SELECT * FROM users WHERE id=?"
        result = cursor.execute(
            query, (_id,)
        )  # user comma to indicate that this is a tuple, not a bracket that prioritize the execution of variables inside it.
        row = result.fetchone()
        if row:
            # user = cls(row[0], row[1], row[2])
            user = cls(*row)
        else:
            user = None

        connection.close()
        return user


# to post users in the database, create an endpoint
class UserRegister(Resource):
    parser = reqparse.RequestParser()  # it's in the class, not in any method
    parser.add_argument(
        "username",
        type=str,
        required=True,  # no request can come through without price
        help="This field cannot be left blank!",
    )
    parser.add_argument(
        "password",
        type=str,
        required=True,  # no request can come through without price
        help="This field cannot be left blank!",
    )

    def post(self):

        data = UserRegister.parser.parse_args()

        connection = sqlite3.connect("data.db")
        cursor = connection.cursor()
        query = "INSERT INTO users VALUES (NULL, ?, ?)"
        cursor.execute(
            query,
            (
                data["username"],
                data["password"],
            ),
        )

        connection.commit()
        connection.close()

        return {"message": "User created successfully."}, 201  # created
