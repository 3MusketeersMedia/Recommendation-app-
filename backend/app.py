import time
import json

from flask import Flask
from flask import request, jsonify
from flask_cors import CORS
import database

# TA email: yogolan@ucsc.edu
# .\venv\Scripts\activate

# instance of flask web app
app = Flask(__name__)
cors = CORS(app)

# attributes currently: movie name, media type, id
def convert_tuple(tuple1):
    item_js = {
        "name": tuple1[0],
        "type": tuple1[1],
        "id": tuple1[2]
    }

    return item_js

# items in list are tuples
# json.dumps() converts tuples to arrays
# all the values in the array are converted to strings
# structure: {"movie name": (json array of attributes)}
def format_media(list1):
    json1 = []
    for item in list1:
        item_js = convert_tuple(item)
        json1.append(item_js)
    
    return jsonify(json1)

def format_user_info():
    pass

# gives the route to the function
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # could check the json to determine which function to implement
        pass
    return "West virgina Country Roads"

@app.route("/movies", methods=['GET'])
def movies():
    db_amazon = database.open_DBConnection()
    all_media = database.get_all(db_amazon, "media")
    dict1 = format_media(all_media)
    return dict1

# need to know what to search for
@app.route("/search")
def search():
    return "search"

@app.route("/login", methods=['POST'])
def login():
    if request.method == 'POST':
        pass
    return "login"

@app.route("/time")
def time():
    return {"time": time.time()}

if __name__ == "__main__":
    app.run(debug=True)
