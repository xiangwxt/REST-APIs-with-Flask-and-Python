# import sqlite3
from db import db

# It's a helper that contains some methods.
# to look up users already stored in the data base
class UserModel(db.Model):

    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    password = db.Column(db.String(80))
    # the column names must match the variable names to be saved in the database
    def __init__(self, username, password):
        # self.id = _id  # id is a python keyword, we don't need to do it, the sql engine will do it
        self.username = username
        self.password = password
        # self.something = "hi"  # this won't be stored in the database

    def save_to_db(self):
        db.session.add(self)  # or db.session.delete(self)
        db.session.commit()

    @classmethod  # without hard coding the class name there
    def find_by_username(cls, username):
        return cls.query.filter_by(
            username=username
        ).first()  # first row then get converted to a UserModel obj

    @classmethod
    def find_by_id(cls, _id):
        return cls.query.filter_by(id=_id).first()
