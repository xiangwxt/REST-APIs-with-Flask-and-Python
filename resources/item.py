from flask_restful import Resource, reqparse
from flask_jwt import jwt_required

# import sqlite3
from models.item import ItemModel


class Item(Resource):

    parser = reqparse.RequestParser()  # it's in the class, not in any method
    parser.add_argument(
        "price",
        type=float,
        required=True,  # no request can come through without price
        help="This field cannot be left blank!",
    )  # make sure nothing else get parsed

    parser.add_argument(
        "store_id",
        type=int,
        required=True,  # no request can come through without price
        help="Every item needs a store id.",
    )

    @jwt_required()
    def get(self, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()  # item is a ItemModel obj
        return {"message": "Item not found"}, 404

    def post(self, name):
        if ItemModel.find_by_name(name):
            return {
                "message": "An item with name '{}' already exists.".format(name)
            }, 400

        data = Item.parser.parse_args()
        # item = {"name": name, "price": data["price"]} # dict
        item = ItemModel(name, data["price"], data["store_id"])

        try:
            # ItemModel.insert(item)
            item.save_to_db()
        except:
            return {
                "message": "An error occured inserting the item."
            }, 500  # internal server error. It's not the user's fault.

        return item.json(), 201

    def delete(self, name):
        # connection = sqlite3.connect("data.db")
        # cursor = connection.cursor()
        # query = "DELETE FROM items WHERE name=?"
        # cursor.execute(query, (name,))
        # connection.commit()
        # connection.close()
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": "Item deleted."}

        return {"message": "Item not found."}, 404

    def put(self, name):
        # data = request.get_json()
        data = Item.parser.parse_args()
        item = ItemModel.find_by_name(name)
        if not item:
            item = ItemModel(name, data["price"], data["store_id"])  # or **data
        else:
            item.price = data["price"]
            item.store_id = data["store_id"]
        item.save_to_db()
        return item.json()


class ItemList(Resource):
    def get(self):

        return {
            "items": [item.json() for item in ItemModel.query.all()]
        }  # return all the objects in the db
        # return {
        #    "items": list(map(lambda x: x.json(), ItemModel.query.all()))
        # } if you are working with other languages than python
