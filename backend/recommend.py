import pandas as pd
import numpy as np
import random
import database
import sklearn
import time
from sklearn.decomposition import TruncatedSVD

# add randomness element?
# Based on items you have liked, watched, rated, viewed?, series?, new?
# Recent history feasible?
# Movielens dataset
# Calculate SVD and then use pearson


# ratings cannot be 0 or function has divide by zero warning
# user_id: user id; media_id: media id to compare; num: number of recommendations to return
def get_user_ratings(pair, user_id, media_id, mediaType='Movie', num=15):
    pair[1].execute("SELECT user_id, media_id, rating FROM preferences WHERE media_id IN (SELECT ID FROM media WHERE mediaType = %s);", (mediaType,))

    table = pair[1].fetchall()
    table = [(a, b, int(c)) for a, b, c in table]

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating"])

    # pivot the table togethers
    rating_table = df.pivot_table(values='rating', index='user_id', columns='media_id', fill_value=0)

    # transpose the pivot table of combined movies
    tranpose = rating_table.T

    # calculate singular value decomposition (SVD) and 
    # scale the resulting matrix from the SVD and transpose
    SVD = TruncatedSVD(n_components=2, random_state=5)
    resultant_matrix = SVD.fit_transform(tranpose)

    # returns the pearson product-moment correlation coefficients
    corr_matrix = np.corrcoef(resultant_matrix)

    # "Star Wars (1977)"; "4154756"
    col_idx = rating_table.columns.get_loc(media_id)
    corr_specific = corr_matrix[col_idx]

    rt = pd.DataFrame({'corr_specific':corr_specific, 'Movies': rating_table.columns}).sort_values('corr_specific', ascending=False).head(num)
    recommended_movies = rt['Movies'].tolist()

    return recommended_movies


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
    corr_mat = np.corrcoef(resultant_matrix)

    col_idx = df2.columns.get_loc("0068646")
    corr_specific = corr_mat[col_idx]

    df3 = pd.DataFrame({'corr_specific':corr_specific, 'media_id': df2.columns}).sort_values('corr_specific', ascending=False).head(10)


# main execution for testing
#db = database.open_DBConnection()
#get_user_rating(db, "3", "0068646", "Movie")
#get_user_rating(db, "3", "3")


# get_user_rating: access movielens 100k dataset
"""
columns = ['user_id', 'item_id', 'rating', 'timestamp']
df = pd.read_csv("u.data", sep='\t', names=columns)

columns = ['item_id', 'movie title', 'release date', 'video release date', 'IMDb URL', 'unknown', 'Action', 'Adventure',
        'Animation', 'Childrens', 'Comedy', 'Crime', 'Documentary', 'Drama', 'Fantasy', 'Film-Noir', 'Horror',
        'Musical', 'Mystery', 'Romance', 'Sci-Fi', 'Thriller', 'War', 'Western']
        
movies = pd.read_csv("u.item", sep='|', names=columns, encoding='latin-1')
movie_names = movies[['item_id', 'movie title']]
combined_movies_data = pd.merge(df, movie_names, on='item_id')
"""
