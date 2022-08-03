# Need to use python 3.9 to use flask_jwt package
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate, identity  # from security.py import two functions
from user import UserRegister
from item import Item, ItemList

# JWT: json web token.
app = Flask(__name__)
app.secret_key = "thea"  # If this were used in production, it would have been long and complicated.  # not used in anywhere
api = Api(app)

jwt = JWT(app, authenticate, identity)

api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")

if (
    __name__ == "__main__"
):  # if we import this file from other places, we don't want to run the file
    app.run(port=5000, debug=True)
