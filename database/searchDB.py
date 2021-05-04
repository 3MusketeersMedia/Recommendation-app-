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
            maxRate = 11
        else:
            maxRate = minRate
    # Since genre can't be generalized like the params, above, must have two possible queries

    if genre != "":
        pair[1].execute("SELECT * FROM media WHERE POSITION(%s in genres) > 0 AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (genre, minYear, maxYear, minRate, maxRate))
    else:
        pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (minYear, maxYear, minRate, maxRate))
    return pair[1].fetchall()