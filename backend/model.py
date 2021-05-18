import pandas as pd
import numpy as np
import collections
import Stemmer
import random
import re
import string

#pip install PyStemmer

STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", 'haven', "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

PUNCTUATION = re.compile('[%s]' % re.escape(string.punctuation))

STEMMER = Stemmer.Stemmer('english')

def tokenize(text):
    return text.split()


def lowercase_filter(tokens):
    return [token.lower() for token in tokens]


def stem_filter(tokens):
    return STEMMER.stemWords(tokens)


def punctuation_filter(tokens):
    return [PUNCTUATION.sub('', token) for token in tokens]


def stopword_filter(tokens):
    return [token for token in tokens if token not in STOPWORDS]


def filter(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = stem_filter(tokens)

    return [token for token in tokens if token]


def search_media_table(pair, query):
    #filter
    filtered_query = filter(query)
    pair[1].execute("SELECT * FROM media WHERE name LIKE %s;", (query,))
    exact = pair[1].fetchall()

    #get list, we are going to add the exact match at the end as the first result
    #so make sure that it isnt the same movie as exact match
    results = []
    for i in filtered_query:
        tmp = "%" + i + "%"
        if len(exact) > 0:
            pair[1].execute("SELECT * FROM media WHERE name LIKE %s AND ID <> %s;", (tmp, exact[0][8]))
        else:
            pair[1].execute("SELECT * FROM media WHERE name LIKE %s;", (tmp,))
        results += pair[1].fetchall()
    
    #sort list by frequency of tuple
    end = [key for key, value in collections.Counter(results).most_common()]
    
    #add exact match as first result if it exists
    if len(exact) > 0:
        end = exact + end
    return end


def advanced_search_media_table(pair, query, genre, yearStart, ratingMin, yearEnd, ratingMax):
    # Checks invalid input, returns empty list if they give some stupid input
    yearStartInvalid = (yearStart != None and not yearStart.isnumeric() and yearStart.strip() != "")
    yearEndInvalid = (yearEnd != None and not yearEnd.isnumeric() and yearEnd.strip() != "")
    ratingMinInvalid = (ratingMin != None and not ratingMin.isnumeric() and ratingMin.strip() != "")
    ratingMaxInvalid = (ratingMax != None and not ratingMax.isnumeric() and ratingMax.strip() != "")
    if (yearStartInvalid or yearEndInvalid or ratingMinInvalid or ratingMaxInvalid):
        return []

    # Checks for empty string being passed in (BTW, default args don't work since it's not NOTHING that's being passed in, it's an empty string--> doesn't default)
    if yearStart == "" or yearStart == None:
        yearStart = "0"
    if yearEnd == "" or yearEnd == None:
        yearEnd = "2050"
    if ratingMin == "" or ratingMin == None:
        ratingMin = "0"
    if ratingMax == "" or ratingMax == None:
        ratingMax = "10"

    results = []
    if(query != "" and query != None):
        filtered_query = filter(query.strip())
        if(genre != "" and genre != None):
            tmp2 = "%" + genre.lower().strip() + "%"
            for i in filtered_query:
                tmp = "%" + i + "%"
                pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND LOWER(genres) LIKE %s;", (tmp, yearStart, yearEnd, ratingMin, ratingMax, tmp2))
                results += pair[1].fetchall()
        else:
            for i in filtered_query:
                tmp = "%" + i + "%"
                pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (tmp, yearStart, yearEnd, ratingMin, ratingMax))
                results += pair[1].fetchall()
    else:
        if(genre != "" and genre != None):
            tmp2 = "%" + genre.strip() + "%"
            pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND LOWER(genres) LIKE %s;", (yearStart, yearEnd, ratingMin, ratingMax, tmp2))
            results += pair[1].fetchall()
        else:
            pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (yearStart, yearEnd, ratingMin, ratingMax))
            results += pair[1].fetchall()
    
    #sort list by frequency of tuple
    return [key for key, value in collections.Counter(results).most_common()]


def get_user_recommendations(pair, user_id):

    pair[1].execute("SELECT user_id, media_id, rating, watched, liked FROM preferences;")
    table = pair[1].fetchall()

    table = [(a, b, int(c), int(d)*2, int(e)*3) for a,b,c,d,e in table] 

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating", "watched", "liked"])
    allRatings = df.pivot_table(index=['user_id'], columns=['media_id'], values=['rating', 'watched', 'liked'])
    
    #evaluate all correlation combos -> as more users increase min_periods
    corrMatrix = allRatings.corr(method='pearson', min_periods = 2)
    
    #get correlation for user
    myRatings = allRatings.loc[user_id].dropna()
    
    simCandidates = pd.Series(dtype='object')
    
    for i in range(0, len(myRatings.index)):
        #print ("Adding sims for " + myRatings.index[i] + "...")
        # Retrieve similar movies to this one that I rated
        sims = corrMatrix[myRatings.index[i]].dropna()
        # Now scale its similarity by how well I rated this movie
        sims = sims.map(lambda x: (x**2) * myRatings[i])
        # Add the score to the list of similarity candidates
        simCandidates = simCandidates.append(sims)

    #sort values and drop movies already rated
    simCandidates.sort_values(inplace = True, ascending = False)
    temp = pd.MultiIndex.from_tuples([('rating', value) for key,value in myRatings.index], names=[None, 'media_id'])
    try:
        filteredSims = simCandidates.drop(temp)
    except:
        filteredSims = simCandidates

    #return list of ids
    end = [value for value in [value for key,value in filteredSims.index.array] if value not in [value for key,value in myRatings.index]]
    return([key for key,value in collections.Counter(end).most_common()])
    #return([value for key,value in [key for key,value in collections.Counter(filteredSims.index.array).most_common()]])

"""
#load file
exec(open("../database/database.py").read())
random.seed(0)

conn = open_DBConnection()

list_movies = get_all(conn)

#add a bunch of users
add_user(conn, "username", "password_hash", "password_salt", "0")
add_user(conn, "username", "password_hash", "password_salt", "1")
add_user(conn, "username", "password_hash", "password_salt", "2")
add_user(conn, "username", "password_hash", "password_salt", "3")
add_user(conn, "username", "password_hash", "password_salt", "4")

#set a bunch of user preferences
ids = ["0", "1", "2", "3", "4"]

z = 5 
for i in ids:
    for x in range(z):
        set_preference(conn, True, True, i, list_movies[x][8], rating=random.randint(0, 10))
    z+=1


#get movie_id, user_id and rating and name
print(get_user_recommendations(conn, "0"))

clear_data(conn, "preferences")
clear_data(conn, "users")

close_DBConnection(conn)
"""
