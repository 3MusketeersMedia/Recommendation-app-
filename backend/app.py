import time
import json

from flask import Flask
from flask import redirect, url_for, request
import database

# TA email: yogolan@ucsc.edu

# instance of flask web app
app = Flask(__name__)

# sample json format
data = {
    "person1": {"name": "rick", "age": 16},
    "person2": {"name": "astley", "age": 65}
}

# items in list are tuples
# keys of the dictionary will be the movie name
# json.dumps() converts tuples to arrays
# all the values in the array are converted to strings apparently - problem?
def format_media(list1):
    json1 = {}
    for item in list1:
        name = item[0]
        js_item = json.dumps(item)
        json1[name] = js_item
    
    #print(json1)
    return json1

# .\venv\Scripts\activate
# gives the route to the function
@app.route("/", methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        # could check the json to determine which function to implement
        pass
    return "West virgina Country Roads"

@app.route("/movies", methods=['GET'])
def movies():
    # attributes currently: movie name, media type, id
    db_amazon = database.open_DBConnection()
    hello = database.get_all(db_amazon, "media")
    dict1 = format_media(hello)
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
