import json
from datetime import timedelta

from flask import Flask
from flask import request, jsonify, redirect, url_for, Response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import database
import bcrypt

# TA email: yogolan@ucsc.edu
# .\venv\Scripts\activate
# use flask-jwt-extended if you are

# Should I maintain a permanent connection to the database or open/close as needed?

# instance of flask web app
app = Flask(__name__)
cors = CORS(app)
# change secret key and implement refresh tokens
app.config["JWT_SECRET_KEY"] = "super-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(days=1)
jwt = JWTManager(app)

db = database.open_DBConnection(True)

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
    all_media = database.get_all(db, "media")
    dict1 = format_media(all_media)
    return dict1

@app.route("/review", methods=['GET'])
@jwt_required()
def review():
    pass

# frontend sends jwt, I look up user
@app.route("/profile")
@jwt_required()
def profile():
    pass

# add: search, profile

# if user, enter; if not, try again
# ask for query method
# if token, return token. If session, return message "login success"
@app.route("/login", methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # query database
    # need to pull hash and salt from db, then hash the password passed in
    # encode utf-8?
    # get entire row or individually?
    user = database.check_user_exists(db, username)
    if not user:
        return jsonify({"msg": "Invalid username or password"})


    hashed = database.get_user_hash(db, username)
    #print(hashed[0].encode("utf-8"))
    if not bcrypt.checkpw(password.encode("utf-8"), hashed[0].encode("utf-8")):
        #print("bad password")
        return jsonify({"msg": "Invalid username or password"})
    
    # if bcrypt.hashpw(password, stored_hash) == stored hash
        
    access_token = create_access_token(identity=username)
    return jsonify({"token": access_token, "username": username})

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
        username = request.json.get("username")
        password = request.json.get("password")
        # existing user check
        # check if password length long?
        if database.check_user_exists(db, username):
            return jsonify({"msg": "Invalid username or password"})
        
        # salt stored as part of hash, do not need to store in database
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

        #print("hash value is: ")
        #print(hashed.decode("utf-8"))

        database.add_user(db, username, hashed.decode("utf-8"), salt)

        # send token
        access_token = create_access_token(identity=username)
        return jsonify({"token": access_token, "username": username})

    return "signup"

if __name__ == "__main__":
    app.run(debug=True)
