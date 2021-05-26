import json
import simplejson
from datetime import timedelta

from flask import Flask
from flask import request, jsonify, redirect, url_for, Response
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from recommend import get_user_ratings
from model import get_user_recommendations
import database
import bcrypt

# check through and run through all functions thoroughly

# TA email: yogolan@ucsc.edu
# .\venv\Scripts\activate
# JWT token: user id, access token
# maybe token dates i.e. timestamp

# Connection pools are backlog
# Require us to rewrite the database api

# try: execute db function (exclude open_connection)

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
    try:
        all_media = database.get_all(db, "media")
        dict1 = format_media(all_media)
    finally:
        database.close_DBConnection(db)

    return dict1

# standard search by name function
@app.route("/search", methods=["POST"])
def search():
    db = database.open_DBConnection()
    result = []
    try:
        searchContents = request.json.get("searchContents", None)
        limit = request.json.get("limit", 50)
        offset = request.json.get("offset", 0)
        result = database.search_media_table(db, searchContents, limit, offset)
    finally:
        database.close_DBConnection(db)

    media = format_media(result['movies'])
    return {
        'movies': media.json,
        'count': result['count']
    }

# advanced search
@app.route("/advSearch", methods=["POST"])
def advSearch():
    result = []
    name = request.json.get("name", None)
    mediaType = request.json.get("mediaType", None)
    genre = request.json.get("genre", None)
    minYear = request.json.get("minYear", None)
    maxYear = request.json.get("maxYear", None)
    minRate = request.json.get("minRate", None)
    maxRate = request.json.get("maxRate", None)
    limit = request.json.get("limit", 50)
    offset = request.json.get("offset", 0)
    db = database.open_DBConnection()
    try:
        media = database.advanced_search_media_table(db, name, mediaType, genre, minYear, minRate, maxYear, maxRate, limit, offset)
        result = format_media(media['movies']).json
    finally:
        database.close_DBConnection(db)

    return jsonify({
        'movies': result,
        'count': media['count']
    })


@app.route("/pages", methods=['GET'])
def pages():
    limit = request.args.get('limit', 100)
    offset = request.args.get('offset', 0)
    pair = database.open_DBConnection(True)
    try:
        pair[1].execute('SELECT * FROM media LIMIT %s OFFSET %s', [limit, offset])
        media = pair[1].fetchall()
        num = database.num_items(pair, 'media')
    finally:
        database.close_DBConnection(pair)

    return jsonify({
        'movies': json.loads(simplejson.dumps(media)),
        'count': num
    })


@app.route('/movieCount')
def movieCount():
    db = database.open_DBConnection()
    try:
        num = database.num_items(db, 'media')
    finally:
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
    try:
        if(database.check_preference(db, user_id, media_id)):
            database.set_data_review(db, user_id, media_id, review)
        else:
            database.set_preference(db, False , False, user_id, media_id, 0, review)
    finally:
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
    try:
        attributes = database.get_by_id(db, user_id, "users")
    finally:
        database.close_DBConnection(db)

    return jsonify({"username": attributes[0]}), 200


@app.route("/rating", methods=["POST"])
@jwt_required()
def rating():
    identity = get_jwt_identity()
    user_id = identity[0]

    media_id = request.json.get("media_id")
    rating = request.json.get("rating")
    #print(rating)
    db = database.open_DBConnection()
    try:
        if(database.check_preference(db, user_id, media_id)):
            database.set_data_rating(db, user_id, media_id, rating)
        else:
            database.set_preference(db, False , False, user_id, media_id, rating, "")
    finally:
        database.close_DBConnection(db)

    return "Rating posted", 200


@app.route("/favorite", methods=["POST", "GET", "DELETE"])
@jwt_required()
def favorite():
    identity = get_jwt_identity()
    user_id = identity[0]
    db = database.open_DBConnection()

    if request.method == "POST":
        media_id = request.json.get("id")

        # if id does not exist, add to database with set_preference
        try:
            if(database.check_preference(db, user_id, media_id)):
                database.set_data_liked(db, user_id, media_id, True)
            else:
                database.set_preference(db, False , True, user_id, media_id)
        finally:
            database.close_DBConnection(db)

        return "Movie favorited", 200
    elif request.method == "DELETE":
        media_id = request.json.get("id")

        # if id does not exist, add to database with set_preference
        try:
            if(database.check_preference(db, user_id, media_id)):
                database.set_data_liked(db, user_id, media_id, False)
            else:
                database.set_preference(db, False , False, user_id, media_id)
        finally:
            database.close_DBConnection(db)

        return "Movie unfavorited", 200
    elif request.method == "GET":
        try:
            fav_movies = database.get_user_liked(db, user_id, True)
        finally:
            database.close_DBConnection(db)

        fav_movies = format_media(fav_movies)
        return fav_movies, 200

    database.close_DBConnection(db)
    return "Method not supported", 403


# get_user_recommendations returns a list
# this is for overall recommendations in profile
@app.route("/user_recommendation", methods=['GET'])
@jwt_required()
def user_recommendation():
    identity = get_jwt_identity()
    user_id = identity[0]
    db = database.open_DBConnection()

    try:
        movies = get_user_recommendations(db, user_id)
    finally:
        database.close_DBConnection(db)

    return jsonify(movies), 200


# targetted recommendations
# first item in list is most recommended
# returns json array of objects
@app.route("/movie_recommendation", methods=['GET'])
@jwt_required()
def movie_recommendation():
    identity = get_jwt_identity()
    user_id = identity[0]
    media_id = request.json.get("media_id")
    mediaType = request.json.get("mediaType")
    #num = request.json.get("num")

    db = database.open_DBConnection()
    try:
        movies = get_user_ratings(db, user_id, media_id, mediaType)
    finally:
        database.close_DBConnection(db)

    return jsonify(movies), 200


@app.route("/watchlist", methods=["POST", "GET", "DELETE"])
@jwt_required()
def watchlist():
    identity = get_jwt_identity()
    user_id = identity[0]
    db = database.open_DBConnection()

    if request.method == "POST":
        media_id = request.json.get("id")

        # if id does not exist, add to database with set_preference
        try:
            if(database.check_preference(db, user_id, media_id)):
                database.set_data_watched(db, user_id, media_id, True)
            else:
                database.set_preference(db, True , False, user_id, media_id)
        finally:
            database.close_DBConnection(db)

        return "Movie watched", 200
    elif request.method == "DELETE":
        media_id = request.json.get("id")

        # if id does not exist, add to database with set_preference
        try:
            if(database.check_preference(db, user_id, media_id)):
                database.set_data_watched(db, user_id, media_id, False)
            else:
                database.set_preference(db, False , False, user_id, media_id)
        finally:
            database.close_DBConnection(db)

        return "Movie unwatched", 200
    elif request.method == "GET":
        try:
            watched = database.get_user_watched(db, user_id, True)
        finally:
            database.close_DBConnection(db)

        watched = format_media(watched)
        return watched, 200


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
    try:
        user = database.check_user_exists(db, username)
    finally:
        database.close_DBConnection(db)

    if not user:
        database.close_DBConnection(db)
        return jsonify({"msg": "Invalid username or password"})

    # validate password
    db = database.open_DBConnection()
    try:
        hashed = database.get_user_hash(db, username)
    finally:
        database.close_DBConnection(db)

    if not bcrypt.checkpw(password.encode("utf-8"), hashed[0].encode("utf-8")):
        database.close_DBConnection(db)
        return jsonify({"msg": "Invalid username or password"})

    db = database.open_DBConnection()
    try:
        user_id = database.get_user_id(db, username)
    finally:
        database.close_DBConnection(db)

    # return token
    access_token = create_access_token(identity=user_id)
    return jsonify({"token": access_token, "id": user_id, "username": username})


# if user, user already exists
# do I need to check if user already signed in?
@app.route("/signup", methods=['POST'])
def signup():
    username = request.json.get("username")
    password = request.json.get("password")
    db = database.open_DBConnection()

    # existing user check
    # check if password length long?
    if database.check_user_exists(db, username):
        database.close_DBConnection(db)
        return jsonify({"msg": "Invalid username or password"})

    # salt stored as part of hash, do not need to store in database
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode("utf-8"), salt)

    #print("hash value is: ")
    #print(hashed.decode("utf-8"))

    try:
        database.add_user(db, username, hashed.decode("utf-8"))
        user_id = database.get_user_id(db, username)
    finally:
        database.close_DBConnection(db)

    # send token
    access_token = create_access_token(identity=user_id)
    return jsonify({"token": access_token, "id": user_id, "username": username})


if __name__ == "__main__":
    app.run(debug=True)
