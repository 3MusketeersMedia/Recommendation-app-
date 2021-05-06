import json
import simplejson
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
# JWT token: user id, access token
# maybe token dates i.e. timestamp

# instance of flask web app
app = Flask(__name__)
cors = CORS(app)
# change secret key and implement refresh tokens
app.config["JWT_SECRET_KEY"] = "super-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# connection to database constantly maintained
db = database.open_DBConnection()

# number of attributes: 9
# user based collaborative filtering or item based collaborative filtering
# get what they watched and rated and get probability of what they watched and returned, highest one
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
def format_media(list1):
    json1 = []
    for item in list1:
        item_js = convert_tuple(item)
        json1.append(item_js)

    return jsonify(json1)


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

# standard search by name function
@app.route("/search", methods=["POST"])
def search():
    #to_return = format_media(database.get_all(db,"media"))
    to_return = format_media(database.get_by_name(db, request.json.get("searchContents", None)))
    return to_return


# advanced search
@app.route("/advSearch", methods=["POST"])
def advSearch():
    genre = request.json.get("genre", None)
    minYear = request.json.get("minYear", None)
    maxYear = request.json.get("maxYear", None)
    minRate = request.json.get("minRate", None)
    maxRate = request.json.get("maxRate", None)
    #media = database.advanced_search(db, genre, minYear, maxYear, minRate, maxRate)
    media = database.get_by_genre(db, genre)
    to_return = format_media(media)
    return to_return


@app.route("/pages", methods=['GET'])
def pages():
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)
    pair = database.open_DBConnection(True)
    pair[1].execute('SELECT * FROM media LIMIT %s OFFSET %s', [limit, offset])
    media = pair[1].fetchall()
    return jsonify(json.loads(simplejson.dumps(media)))


@app.route('/movieCount')
def movieCount():
    pair = database.open_DBConnection()
    return jsonify(database.num_items(pair, 'media'))


@app.route("/review", methods=['GET'])
@jwt_required()
def review():
    pass


# frontend sends jwt, I look up user
@app.route("/profile")
@jwt_required()
def profile():
    identity = get_jwt_identity()
    print(identity)

    # new function, I do not want to grab the password hash
    attributes = database.get_by_id(db, identity[0], "users")
    print(attributes)
    return jsonify({"username": attributes[0]}), 200


@app.route("/favorite", methods=["POST", "GET"])
@jwt_required()
def favorite():
    if request.method == "POST":
        pass
    identity = get_jwt_identity()
    print(identity)

    return "hello"


# protects a route with jwt_required
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    return jsonify(logged=current_user), 200


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
    # get entire row or just attribute?
    user = database.check_user_exists(db, username)
    if not user:
        return jsonify({"msg": "Invalid username or password"})

    # validate password
    hashed = database.get_user_hash(db, username)
    if not bcrypt.checkpw(password.encode("utf-8"), hashed[0].encode("utf-8")):
        return jsonify({"msg": "Invalid username or password"})

    # if bcrypt.hashpw(password, stored_hash) == stored hash
    user_id = database.get_user_id(db, username)

    # return token    
    access_token = create_access_token(identity=user_id)
    return jsonify({"token": access_token, "id": user_id, "username": username})


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

        database.add_user(db, username, hashed.decode("utf-8"))
        user_id = database.get_user_id(db, username)

        # send token
        access_token = create_access_token(identity=user_id)
        return jsonify({"token": access_token, "id": user_id, "username": username})

    return "signup"


if __name__ == "__main__":
    app.run(debug=True)
