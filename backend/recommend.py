import pandas as pd
import numpy as np
import random
import database
import sklearn
import time
from sklearn.decomposition import TruncatedSVD

# Strategy: get a couple of watched genres for user
# Recommend movies that are similar  to what you look at
# randomness element
# Based on items you have liked, watched, rated, viewed?, series?, new?
# Recent history feasible?

# Movielens dataset
# Calculate SVD and then use cosine or pearson

def filter_seen_movies(pair, user_id):
    # pass in table or matrix
    # if filter recomm list, list could be small
    # if entire table, need to loop through entire table
    pass


def get_user_rating(pair, user_id, media_id):
    #start = time.time()
    columns = ['user_id', 'item_id', 'rating', 'timestamp']
    df = pd.read_csv("u.data", sep='\t', names=columns)
    #print(df)

    columns = ['item_id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
          'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
          'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
          
    movies = pd.read_csv("u.item", sep='|', names=columns, encoding='latin-1')
    #print(movies.loc[df["item_id"] == "1398"])
    movie_names = movies[['item_id', 'movie title']]
    combined_movies_data = pd.merge(df, movie_names, on='item_id')

    # pivot the table together
    rating_crosstab = combined_movies_data.pivot_table(values='rating', index='user_id', columns='movie title', fill_value=0)
    #print(rating_crosstab)

    # transpose the pivot table of combined movies
    tranpose = rating_crosstab.T

    # calculate singular value decomposition and scale the resulting matrix from the SVD and transpose
    SVD = TruncatedSVD(n_components=12, random_state=5)
    resultant_matrix = SVD.fit_transform(tranpose)

    # returns the pearson product-moment correlation coefficients
    corr_mat = np.corrcoef(resultant_matrix)

    # item id of star wars = 50; need to return media_id
    col_idx = rating_crosstab.columns.get_loc("Star Wars (1977)")
    corr_specific = corr_mat[col_idx]
    #print(corr_specific)
    rt = pd.DataFrame({'corr_specific':corr_specific, 'Movies': rating_crosstab.columns}).sort_values('corr_specific', ascending=False).head(20)
    #end = time.time()
    #print(end - start)
    #print(rt)


def get_user_likes(pair, user_id, media_id):
    pair[1].execute("SELECT user_id, media_id, liked FROM preferences;")
    # check if table has values or not
    table = pair[1].fetchall()

    table = [(a, b, int(c)) for a,b,c in table]

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "liked"])
    df2 = df.pivot_table(index=['user_id'], columns=['media_id'], values='liked', fill_value=0)

    X = df2.T

    SVD = TruncatedSVD(n_components=3, n_iter=3, random_state=8)

    resultant_matrix = SVD.fit_transform(X)
    #print(resultant_matrix)
    corr_mat = np.corrcoef(resultant_matrix)

    col_idx = df2.columns.get_loc("0068646")
    corr_specific = corr_mat[col_idx]

    df3 = pd.DataFrame({'corr_specific':corr_specific, 'media_id': df2.columns}).sort_values('corr_specific', ascending=False).head(10)
    #print(df3)


"""
# main execution for testing
db = database.open_DBConnection()
#list_movies = database.get_all(db)
#db = 3

get_user_rating(db, "3", "0068646")
#get_user_likes(db, "3", "0068646")
"""
