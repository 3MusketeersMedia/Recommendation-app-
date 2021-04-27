import time
import json

from flask import Flask
from flask import request, jsonify, redirect, url_for, Response
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import database

# TA email: yogolan@ucsc.edu
# .\venv\Scripts\activate
# use flask-jwt-extended if you are

# Should I maintain a permanent connection to the database or open/close as needed?

# instance of flask web app
app = Flask(__name__)
cors = CORS(app)
app.config["JWT_SECRET_KEY"] = "super-key"
jwt = JWTManager(app)

# number of attributes currently: 9
# attributes currently: movie name, media type, id
def convert_tuple(tuple1):
    item_js = {
        "name": tuple1[0],
        "mediaType": tuple1[1],
        "year": tuple1[2],
        "link": tuple1[3],
        "genres": tuple1[4],
        "rating": str(tuple1[5]),
        "running_time": str(tuple1[6]),
        "summary": tuple1[7],
        "id": tuple1[8]
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

# too many movies, need to split it off
@app.route("/movies", methods=['GET'])
def movies():
    db_amazon = database.open_DBConnection(True)
    # need to close db connection?
    all_media = database.get_all(db_amazon, "media")
    database.close_DBConnection(db_amazon)
    dict1 = format_media(all_media)
    return dict1

# add: search, profile

# if user, enter; if not, try again
# ask for query method
# if token, return token. If session, return message "login success"
@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        username = request.json.get("username", None)
        password = request.json.get("password", None)
        print(username)
        print(password)

        # query database
        db = database.open_DBConnection(True)
        user = database.check_user_exists(db, username)

        if not user:
            print("bad msg")
            return jsonify({"msg": "Invalid username or password"})
        
        access_token = create_access_token(identity=username)
        return jsonify({"token": access_token, "username": username})
    
    return "hello"

# protects a route with jwt_required
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged=current_user), 201

# if user, user already exists
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("password")
        # existing user check
    return "signup"

@app.route("/protected/time")
def time():
    return "hello"
    #return {"time": time.time()}

if __name__ == "__main__":
    app.run(debug=True)
