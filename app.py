# Need to use python 3.9 to use flask_jwt package
import os  # access to operating system's environmental variables

from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity  # from security.py import two functions

from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

# the models get imported through the import of resources


# JWT: json web token.
app = Flask(__name__)

from db import db

db.init_app(app)


app.config["SQLAlCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
    "DATABASE_URL_sql", "sqlite:///data.db"
)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///data.db"
# DATABASE_URL: the variable that Heroku created as environment variable, but it's not defined in local
# if the first one is not found, use the second default variable instead
app.secret_key = "thea"
api = Api(app)


@app.before_first_request  # run before the code below it, and run before the first request
def create_tables():  # if we don't import one of the module, the specific table will not be created.
    db.create_all()


jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
api.add_resource(Store, "/store/<string:name>")
api.add_resource(StoreList, "/stores")

if (
    __name__ == "__main__"
):  # if we import this file from other places, we don't want to run the file
    app.run(port=5000, debug=True)
