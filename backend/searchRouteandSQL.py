# I currently have these functions actually in 
# app.py and database.py respectively, but
# here is basically a reference to what I added (for the time being)

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

# standard search by name function
@app.route("/search", methods=["POST"])
def search():
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
    media = database.advanced_search(db, genre.strip(), minYear.strip(), maxYear.strip(), minRat.strip(), maxRate.strip())
    to_return = format_media(media)
    return to_return

def advanced_search(pair, genre, minYear, maxYear, minRate, maxRate):
    # First, some edge case handling (based on user input)
    if maxYear == "":
        if minYear == "":
            minYear = "1500"
            maxYear = "2050"
        else:
            maxYear = minYear
    if maxRate == "":
        if minRate == "":
            minRate = 0
            maxRate = 5
        else:
            maxRate = minRate
    # Since genre can't be generalized like the params, above, must have two possible queries

    if genre != "":
        pair[1].execute("SELECT * FROM media WHERE POSITION(%s in genres) > 0 AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (genre, minYear, maxYear, minRate, maxRate))
    else:
        pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (minYear, maxYear, minRate, maxRate))
    return pair[1].fetchall()
