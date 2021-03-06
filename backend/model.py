import pandas as pd
import numpy as np
import collections
import database
import Stemmer
import random
import re
import string
from spellchecker import SpellChecker

STOPWORDS = set(['i', 'me', 'my', 'myself', 'we', 'our', 'ours', 'ourselves', 'you', "you're", "you've", "you'll", "you'd", 'your', 'yours', 'yourself', 'yourselves', 'he', 'him', 'his', 'himself', 'she', "she's", 'her', 'hers', 'herself', 'it', "it's", 'its', 'itself', 'they', 'them', 'their', 'theirs', 'themselves', 'what', 'which', 'who', 'whom', 'this', 'that', "that'll", 'these', 'those', 'am', 'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has', 'had', 'having', 'do', 'does', 'did', 'doing', 'a', 'an', 'the', 'and', 'but', 'if', 'or', 'because', 'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about', 'against', 'between', 'into', 'through', 'during', 'before', 'after', 'above', 'below', 'to', 'from', 'up', 'down', 'in', 'out', 'on', 'off', 'over', 'under', 'again', 'further', 'then', 'once', 'here', 'there', 'when', 'where', 'why', 'how', 'all', 'any', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such', 'no', 'nor', 'not', 'only', 'own', 'same', 'so', 'than', 'too', 'very', 's', 't', 'can', 'will', 'just', 'don', "don't", 'should', "should've", 'now', 'd', 'll', 'm', 'o', 're', 've', 'y', 'ain', 'aren', "aren't", 'couldn', "couldn't", 'didn', "didn't", 'doesn', "doesn't", 'hadn', "hadn't", 'hasn', "hasn't", "haven't", 'isn', "isn't", 'ma', 'mightn', "mightn't", 'mustn', "mustn't", 'needn', "needn't", 'shan', "shan't", 'shouldn', "shouldn't", 'wasn', "wasn't", 'weren', "weren't", 'won', "won't", 'wouldn', "wouldn't"])

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
    return [token for token in tokens if token not in punctuation_filter(STOPWORDS)]


def spelling_filter(tokens):
    return [SpellChecker().correction(token) for token in tokens]


def filter(text):
    tokens = tokenize(text)
    tokens = lowercase_filter(tokens)
    tokens = punctuation_filter(tokens)
    tokens = spelling_filter(tokens)
    tokens = stopword_filter(tokens)
    tokens = stem_filter(tokens)

    return [token for token in tokens if token]


def search_media_table(pair, query, limit, offset):
    #filter
    filtered_query = filter(query)
    query_check = "%" + query + "%"
    pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE LOWER(%s);", (query_check,))
    exact = pair[1].fetchall()

    #get list, we are going to add the exact match at the end as the first result
    #so make sure that it isnt the same movie as exact match
    results = []
    for i in filtered_query:
        tkn = "%" + i + "%"
        if len(exact) > 0:
            pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE %s AND ID <> %s;", (tkn, exact[0][8]))
        else:
            pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE %s;", (tkn,))
        results += pair[1].fetchall()

    #sort list by frequency of tuple
    end = [key for key, value in collections.Counter(results).most_common()]

    #add exact match as first result if it exists
    if len(exact) > 0:
        end = exact + end
    to_return = [key for key,value in collections.Counter(end).most_common()]
    return {
        'movies': to_return[offset:offset+limit],
        'count': len(to_return)
    }

def advanced_search_media_table(pair, query, mediaType, genre, yearStart, ratingMin, yearEnd, ratingMax, limit, offset):
    # Checks invalid input, returns empty list if they give some stupid
    yearStartInvalid = (yearStart != None and not yearStart.isnumeric() and yearStart.strip() != "")
    yearEndInvalid = (yearEnd != None and not yearEnd.isnumeric() and yearEnd.strip() != "")
    ratingMinInvalid = (ratingMin != None and not ratingMin.isnumeric() and ratingMin.strip() != "")
    ratingMaxInvalid = (ratingMax != None and not ratingMax.isnumeric() and ratingMax.strip() != "")
    if (yearStartInvalid or yearEndInvalid or ratingMinInvalid or ratingMaxInvalid):
        return {
        'movies': [],
        'count': 0
    }

    # Checks for empty string being passed in (BTW, default args don't work since it's not NOTHING that's being passed in, it's an empty string--> doesn't default)
    if yearStart == "" or yearStart == None:
        yearStart = "0"
    if yearEnd == "" or yearEnd == None:
        yearEnd = "2050"
    if ratingMin == "" or ratingMin == None:
        ratingMin = "0"
    if ratingMax == "" or ratingMax == None:
        ratingMax = "10"

    # If statements below are for the cases in which there are no name or no genre input (4 cases)
    results = []
    if(query != "" and query != None):
        filtered_query = filter(query.strip())
        if(genre != "" and genre != None):
            tkn2 = "%" + genre.lower().strip() + "%"
            for i in filtered_query:
                tkn = "%" + i + "%"
                pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND LOWER(genres) LIKE %s;", (tkn, yearStart, yearEnd, ratingMin, ratingMax, tkn2))
                results += pair[1].fetchall()
        else:
            for i in filtered_query:
                tkn = "%" + i + "%"
                pair[1].execute("SELECT * FROM media WHERE LOWER(name) LIKE %s AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (tkn, yearStart, yearEnd, ratingMin, ratingMax))
                results += pair[1].fetchall()
    else:
        if(genre != "" and genre != None):
            tkn2 = "%" + genre.lower().strip() + "%"
            pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s AND LOWER(genres) LIKE %s;", (yearStart, yearEnd, ratingMin, ratingMax, tkn2))
            results += pair[1].fetchall()
        else:
                pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (yearStart, yearEnd, ratingMin, ratingMax))
                results += pair[1].fetchall()

    # The below code removes all results that aren't of the type mediaType (if mediaType specified).
    if mediaType != "" and mediaType != None:
        tkn3 = "%" + mediaType.lower().strip() + "%"
        pair[1].execute("SELECT * FROM media WHERE LOWER(mediaType) LIKE %s;", (tkn3,))
        mediaTypeResults = pair[1].fetchall()
        results = list(set(results).intersection(set(mediaTypeResults))) # Removes what's different between results and mediaTypeResults
    #sort list by frequency of tuple
    toReturn = [key for key, value in collections.Counter(results).most_common()]
    return {
        'movies': toReturn[offset:offset+limit],
        'count': len(toReturn)
    }


def get_user_recommendations(pair, user_id):
    pair[1].execute("SELECT user_id, media_id, rating, watched, liked FROM preferences;")
    table = pair[1].fetchall()

    table = [(a, b, float(c), int(d)*2, int(e)*3) for a,b,c,d,e in table]

    # list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating", "watched", "liked"])
    allRatings = df.pivot_table(index=['user_id'], columns=['media_id'], values=['rating', 'watched', 'liked'])

    # evaluate all correlation combos -> as more users increase min_periods
    corrMatrix = allRatings.corr(method='pearson', min_periods = 2)

    # get correlation for user
    try:
        myRatings = allRatings.loc[user_id].dropna()
    except:
        return []
        
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
    end = [database.get_by_id(pair, key) for key,value in collections.Counter(end).most_common()]
    return end


