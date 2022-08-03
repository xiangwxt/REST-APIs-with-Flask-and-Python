# import sqlite3
from db import db


class ItemModel(db.Model):  # create the mapping between the database and the object

    __tablename__ = "items"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))
    store_id = db.Column(
        db.Integer, db.ForeignKey("stores.id")
    )  # table name: stores, id
    store = db.relationship(
        "StoreModel"
    )  # we can find a store in db that matches the store_id

    def __init__(self, name, price, store_id):
        self.name = name
        self.price = price
        self.store_id = store_id

    def json(self):  # return a json representation of the model
        # as opposed to a dictionary
        return {"name": self.name, "price": self.price}

    @classmethod  # should
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()
        # ItemModel.query.filter_by(name=name).filter_by(id=1) # from the db.Model
        # ItemModel.query.filter_by(name=name).filter_by(id=1).first()
        # ItemModel.query.filter_by(name=name, id=1)
        # select * from items where name = name

    def save_to_db(self):  # it's inserting itself
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "INSERT INTO items VALUES (?, ?)"
        # cursor.execute(query, (self.name, self.price))
        # connection.commit()
        # connection.close()
        db.session.add(
            self
        )  # the session is a collection of obj that we want to add into the db
        db.session.commit()  # sqlalchemy will do an update instead of an insert

    def delete_from_db(self):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "UPDATE items SET price=? WHERE name=?"
        # cursor.execute(query, (self.price, self.name))
        # connection.commit()
        # connection.close()
        db.session.delete(self)
        db.session.commit()
