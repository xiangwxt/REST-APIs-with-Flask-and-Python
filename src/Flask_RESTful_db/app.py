# Need to use python 3.9 to use flask_jwt package
from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required  # a decorator for get method
from security import authenticate, identity  # from security.py import two functions
from user import UserRegister

# JWT: json web token.
app = Flask(__name__)
app.secret_key = "thea"  # If this were used in production, it would have been long and complicated.  # not used in anywhere
api = Api(app)

jwt = JWT(
    app, authenticate, identity
)  # use app and two functions together to allow for authentification of users

# JWT start a new end point, namely /auth
# when we call /auth, we send it a username and a password
# JWT() get the username and password and send them over to the authenticate function,
# that takes username and password, then we find the correct user object
# the /auth endpoint returns a JW token
# the JWT() calls the identity function, and use the JWT to get the user ID, and the correct user

items = []


class Item(Resource):

    parser = reqparse.RequestParser()  # it's in the class, not in any method
    parser.add_argument(
        "price",
        type=float,
        required=True,  # no request can come through without price
        help="This field cannot be left blank!",
    )  # make sure nothing else get parsed

    @jwt_required()  # decorator in front of get method
    # we have to authenticate before calling get method
    def get(self, name):
        item = next(
            filter(lambda x: x["name"] == name, items), None
        )  # return a filter obj
        # next() gives the first item found by this filter function. Can call next again to get the second
        # it will raise an error if there's no item that matches the name. Need to add None, it will return None.
        # list() return all the items that match the filter function, but this one: a list of a single item
        # don't need to use jsonify, flask_restful will do it automatically
        return {"item": item}, 200 if item else 404  # status codes: 404 not found,
        # 201 created, 202: accepted, when you are delaying the creation
        # 200 success

    def post(self, name):
        if next(filter(lambda x: x["name"] == name, items), None):
            return {
                "message": "An item with name '{}' already exists.".format(name)
            }, 400
        # do not need content header, process the text even if it's incorrect
        # silent=True, doesn't give error, just give None
        data = Item.parser.parse_args()
        # data = request.get_json(force=True)
        item = {"name": name, "price": data["price"]}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items  # need to bring in the global variable
        items = list(
            filter(lambda x: x["name"] != name, items)
        )  # exclude the one to be deleted
        # problem: the items is considered as a newly defined local variable, and we cannot use it to define itself
        return {"message": "Item deleted"}

    def put(self, name):
        # data = request.get_json()
        data = (
            Item.parser.parse_args()
        )  # parse the args that come through json payload and put valid ones in data
        # if you other inputs are put, they will get erased.
        item = next(filter(lambda x: x["name"] == name, items), None)  # a dictionary
        if not item:
            item = {"name": name, "price": data["price"]}
            items.append(item)
        else:
            item.update(data)  # may change the item name
        return item


class ItemList(Resource):
    def get(self):
        return {"items": items}


api.add_resource(Item, "/item/<string:name>")
api.add_resource(ItemList, "/items")
api.add_resource(UserRegister, "/register")
app.run(port=5000, debug=True)
