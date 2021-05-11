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


def advanced_search_media_table(pair, query, mediaType, genre, yearStart, ratingMin, yearEnd=-1, ratingMax=-1):
    
    if yearEnd == -1:
        yearEnd = yearStart
    if ratingMax == -1:
        ratingMax = ratingMin

    #filter
    filtered_query = filter(query)
    tmp2 = "%" + mediaType + "%"
    pair[1].execute("SELECT * FROM media WHERE name LIKE %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND mediaType LIKE %s;", (query, yearStart, yearEnd, ratingMin, ratingMax, tmp2))
    exact = pair[1].fetchall()

    #get list, we are going to add the exact match at the end as the first result
    #so make sure that it isnt the same movie as exact match
    results = []
    for i in filtered_query:
        tmp = "%" + i + "%"
        if len(exact) > 0:
            pair[1].execute("SELECT * FROM media WHERE name LIKE %s AND ID <> %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND mediaType LIKE %s;", (tmp, exact[0][8], yearStart, yearEnd, ratingMin, ratingMax, tmp2))
        else:
            pair[1].execute("SELECT * FROM media WHERE name LIKE %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND mediaType LIKE %s;", (tmp, yearStart, yearEnd, ratingMin, ratingMax, tmp2))
        results += pair[1].fetchall()

    #sort list by frequency of tuple
    end = [key for key, value in collections.Counter(results).most_common()]

    #add exact match as first result if it exists
    if len(exact) > 0:
        end = exact + end 
    return end


def get_user_recommendations(pair, user_id):

    pair[1].execute("SELECT user_id, media_id, rating FROM preferences;")
    table = pair[1].fetchall()

    table = [(a, b, int(c)) for a,b,c in table] 

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating"])
    allRatings = df.pivot_table(index=['user_id'], columns=['media_id'], values='rating')
    
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
        sims = sims.map(lambda x: x * myRatings[i])
        # Add the score to the list of similarity candidates
        simCandidates = simCandidates.append(sims)

    #sort values and drop movies already rated
    simCandidates.sort_values(inplace = True, ascending = False)
    filteredSims = simCandidates.drop(myRatings.index)
    
    #return list of ids
    return(list(filteredSims.index.array))


#load file
exec(open("backend/database.py").read())
random.seed(0)

conn = open_DBConnection()

list_movies = get_all(conn)

#add a bunch of users
ids = []
z = 5
for i in range (z):
    # pip install random-username
    username = generate_username(1)
    chars = string.ascii_letters + string.digits + '+/'
    assert 256 % len(chars) == 0  # non-biased later modulo
    PWD_LEN = 16
    password_hash = ''.join(chars[c % len(chars)] for c in os.urandom(PWD_LEN))
    add_user(conn, str(username), password_hash)
    #set a bunch of user preferences
    ids.append(str(i))


#set a bunch of user preferences
# ids = ["0", "1", "2", "3", "4"]


for i in ids:
    for x in range(z):
        set_preference(conn, True, True, i, list_movies[x][8], rating=random.randint(0, 10))
    z+=1


# get movie_id, user_id and rating and name

print(user_recommendations(conn, "0"))

clear_data(conn, "preferences")
clear_data(conn, "users")

close_DBConnection(conn)

