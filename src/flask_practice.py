from flask import Flask # import Flask class

# create an app from Flask class
app = Flask(__name__) # variable gives each file a unique name

# tell app what request is going to understand: the home page of the app
@app.route('/') # the route or the end point that is going to understand 'http://www.google.com/'

def home(): # the name is not important. It has to return something to browser.
    return "Hello, world!"

# port: the area of your computer where your app is going to be receiving your requests and returning your responses through.
app.run(port=5000)
# http://127.0.0.1:5000 127.0.0.1 is a special ip address reserved for your computer


# To run type:
# python flask_practice.py