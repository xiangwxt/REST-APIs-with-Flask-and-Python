from db import db


class StoreModel(db.Model):  # create the mapping between the database and the object

    __tablename__ = "stores"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship("ItemModel", lazy="dynamic")  # a list of ItemModels
    # if not lazy, then whenever we create a store model, we will create an object for each item
    # that matches that store id, it's expensive.

    def __init__(self, name):
        self.name = name

    def json(self):
        return {"name": self.name, "items": [item.json() for item in self.items.all()]}
        # when we use items = db.relationship('ItemModel', lazy='dynamic'), self.items no longer is a list of items,
        # it's a query builder that has the ability to look into the items table,
        # we can use .all() to retrieve the items in the table
        # every time we call this function, it will go to the table, it will be slower.

    # tradeoff for creation of the store and speed of calling the JSON method.
    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save_to_db(self):  # it's inserting itself

        db.session.add(
            self
        )  # the session is a collection of obj that we want to add into the db
        db.session.commit()  # sqlalchemy will do an update instead of an insert

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()
