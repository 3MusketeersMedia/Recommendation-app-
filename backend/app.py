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

# To-do list:
# 1) password hashes are not unique for some reason

# instance of flask web app
app = Flask(__name__)
cors = CORS(app)

# change secret key and implement refresh tokens
app.config["JWT_SECRET_KEY"] = "super-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(days=1)
app.config["JWT_REFRESH_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

# connection to database constantly not maintained
#db = database.open_DBConnection()

# number of attributes: 9
# user based collaborative filtering or item based collaborative filtering
# get what they watched and rated and get probability of what they watched and returned, highest one
def convert_media(tuple1):
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


# Should move these functions to a utility file
def convert_pref(tuple1):
    item_js = {
        "watched": tuple1[0],
        "liked": tuple1[1],
        "rating": str(tuple1[2]),
        "review": tuple1[3],
        "user_id": tuple1[4],
        "media_id": tuple1[5]
    }

    return item_js


# items in list are tuples
# json.dumps() converts tuples to arrays
# all the values in the array are converted to strings
def format_media(db_list):
    json1 = []
    for item in db_list:
        item_js = convert_media(item)
        json1.append(item_js)

    return jsonify(json1)


def format_preferences(db_list):
    json1 = []
    for item in db_list:
        item_js = convert_pref(item)
        json1.append(item_js)

    return json1


@app.route("/", methods=['POST', 'GET'])
def index():
    # could check the json to determine which function to implement if you want
    # to fit multiple functions in one route
    return "West virgina Country Roads"


# too many movies, need to split it off
@app.route("/movies", methods=['GET'])
def movies():
    db = database.open_DBConnection()
    all_media = database.get_all(db, "media")
    database.close_DBConnection(db)
    dict1 = format_media(all_media)
    return dict1

# standard search by name function
@app.route("/search", methods=["POST"])
def search():
    db = database.open_DBConnection()
    to_return = format_media(database.search_media_table(db, request.json.get("searchContents", None)))
    database.close_DBConnection(db)
    return to_return

# advanced search
@app.route("/advSearch", methods=["POST"])
def advSearch():
    name = request.json.get("name", None)
    genre = request.json.get("genre", None)
    minYear = request.json.get("minYear", None)
    maxYear = request.json.get("maxYear", None)
    minRate = request.json.get("minRate", None)
    maxRate = request.json.get("maxRate", None)
    db = database.open_DBConnection()
    media = database.advanced_search_media_table(db, name, genre, minYear, minRate, maxYear, maxRate)
    database.close_DBConnection(db)
    to_return = format_media(media)
    return to_return


@app.route("/pages", methods=['GET'])
def pages():
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)
    pair = database.open_DBConnection(True)
    pair[1].execute('SELECT * FROM media LIMIT %s OFFSET %s', [limit, offset])
    media = pair[1].fetchall()
    database.close_DBConnection(pair)
    return jsonify(json.loads(simplejson.dumps(media)))


@app.route('/movieCount')
def movieCount():
    db = database.open_DBConnection()
    num = database.num_items(db, 'media')
    database.close_DBConnection(db)
    return jsonify(num)


@app.route("/review", methods=["POST"])
@jwt_required()
def review():
    identity = get_jwt_identity()
    user_id = identity[0]

    media_id = request.json.get("media_id")
    review = request.json.get("review")
    db = database.open_DBConnection()
    database.set_data_review(db, user_id, media_id, review)
    database.close_DBConnection(db)

    return "Review posted", 200


# frontend sends jwt, I look up user
# identity returned as list, so need to access it
@app.route("/profile", methods=["GET"])
@jwt_required()
def profile():
    identity = get_jwt_identity()
    user_id = identity[0]

    db = database.open_DBConnection()
    attributes = database.get_by_id(db, user_id, "users")
    database.close_DBConnection(db)

    return jsonify({"username": attributes[0]}), 200


@app.route("/favorite", methods=["POST", "GET", "DELETE"])
@jwt_required()
def favorite():
    identity = get_jwt_identity()
    user_id = identity[0]
    db = database.open_DBConnection()

    if request.method == "POST":
        media_id = request.json.get("id")
        rating = request.json.get("rating")

        # if id does not exist, add to database with set_preference
        if(database.check_preference(db, user_id, media_id)): 
            database.set_data_liked(db, user_id, media_id, True)
        else: 
            database.set_preference(db, False , True, user_id, media_id)
        return "Movie favorited", 200
    elif request.method == "DELETE": 
        media_id = request.json.get("id")

        # if id does not exist, add to database with set_preference
        if(database.check_preference(db, user_id, media_id)): 
            database.set_data_liked(db, user_id, media_id, False)
        else: 
            database.set_preference(db, False , False, user_id, media_id)
        return "Movie unfavorited", 200
    elif request.method == "GET":
        fav_movies = database.get_user_liked(db, user_id, True)
        fav_movies = format_media(fav_movies)
        return fav_movies, 200

    database.close_DBConnection(db)
    return "Method not supported", 403


@app.route("/recommend_movies", methods=['GET'])
@jwt_required()
def recommend_movies():
    pass


@app.route("/watchlist", methods=['GET'])
@jwt_required()
def watchlist():
    identity = get_jwt_identity()
    user_id = identity[0]
    db = database.open_DBConnection()

    watched = database.get_user_watched(db, user_id, True)
    database.close_DBConnection(db)
    watched = format_preferences(watched)
    return jsonify(watched), 200

# 0065392, 0104988

# 2 functions below for testing JWT
# protects a route with jwt_required
@app.route("/protected", methods=["GET"])
@jwt_required()
def protected():
    current_user = get_jwt_identity()
    db = database.open_DBConnection()
    database.set_preference(db, True, False, "3748288412750637086", "0065392", rating=0, review=" ")
    database.close_DBConnection(db)
    return jsonify(logged=current_user), 200


@app.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
def refresh():
    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)
    return jsonify(access_token=access_token)


# if user, enter; if not, try again
# ask for query method
# if token, return token. If session, return message "login success"
@app.route("/login", methods=['POST'])
def login():
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    db = database.open_DBConnection()

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
    database.close_DBConnection(db)
    return jsonify({"token": access_token, "id": user_id, "username": username})


# if user, user already exists
@app.route("/signup", methods=['GET', 'POST'])
def signup():
    if request.method == "POST":
        username = request.json.get("username")
        password = request.json.get("password")
        db = database.open_DBConnection()

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
        database.close_DBConnection(db)
        return jsonify({"token": access_token, "id": user_id, "username": username})

    return "signup"


if __name__ == "__main__":
    app.run(debug=True)
