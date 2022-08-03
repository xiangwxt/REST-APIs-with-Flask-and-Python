from flask import Flask
from flask_restful import (
    Resource,
    Api,
)  # Resource: content that api can return or create

app = Flask(__name__)
api = Api(app)  # to add resource


class Student(Resource):  # Student class is a copy of Resource class
    def get(self, name):
        return {"student": name}


# the resource can only be accessed by get method

api.add_resource(
    Student, "/student/<string:name>"
)  # the resouce: student we've created is accessible via API.
# http://127.0.0.1:5000/student/Rolf
# the same as @app.route('/student/<string:name>')

app.run(port=5000)  # it's default
