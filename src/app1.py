from flask import (
    Flask,
    jsonify,
    request,
    render_template,
)  # convert a dict to json, to look for template

app = Flask(__name__)

# in memory
stores = [
    {"name": "My Wonderful Store", "items": [{"name": "My Item", "price": 15.99}]}
]


@app.route("/")  # the home
def home():
    return render_template("index.html")


# flask auto matically looks into the templates folder and look for the html file

# from a server perspective
# POST - used to receive data
# GET - used to send data back only

# POST / store data: {name:}
@app.route(
    "/store", methods=["POST"]
)  # call this end point, default is GET, # methods=["POST", "GET"]
def create_store():
    request_data = (
        request.get_json()
    )  # request made to this end point, and convert json to py dict
    new_store = {"name": request_data["name"], "items": []}
    stores.append(new_store)
    return jsonify(new_store)  # return a string


# GET /store/<string:name>
@app.route("/store/<string:name>")  # 'http://127.0.0.1:5000/store/some_name'
def get_store(name):
    # Iterate over stores
    # if the store name matches, return it
    # if none match, return an error message
    for store in stores:
        if store["name"] == name:
            return jsonify(store)
        return jsonify({"message": "store not found"})


# Difference between python dictionary and json: json only uses double quotes.

# GET /store
@app.route("/store")
def get_stores():  # the method names need to be unique
    return jsonify(
        {"stores": stores}
    )  # convert stores variable into json, stores is a list, need to be converted to a dict


# POST /store/<string:name>/item {name:, price:}
@app.route("/store/<string:name>/item", methods=["POST"])
def create_item_in_store(name):
    request_data = request.get_json()
    for store in stores:
        if store["name"] == name:
            new_item = {"name": request_data["name"], "price": request_data["price"]}
            store["items"].append(new_item)
            return jsonify(store)  # or new_item, up to the setting of API
    return jsonify({"message": "store not found"})


# GET /store/<string:name>/item   # get all the item in a specific store
@app.route("/store/<string:name>/item")
def get_items_in_store(name):
    for store in stores:
        if store["name"] == name:
            return jsonify({"items": store["items"]})
    return jsonify({"message": "store not found"})


app.run(port=5000)
