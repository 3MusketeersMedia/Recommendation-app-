import pandas as pd
import numpy as np
import database
import sklearn
from sklearn.decomposition import TruncatedSVD
from random import randint

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
    # if no recommendations, default recommendations based on genre
    try:
        col_idx = rating_table.columns.get_loc(media_id)
        corr_specific = corr_matrix[col_idx]

        rt = pd.DataFrame({'corr_specific':corr_specific, 'Movies': rating_table.columns}).sort_values('corr_specific', ascending=False).head(num)
        recommended_movies = rt['Movies'].tolist()

        return recommended_movies
    except KeyError:
        # AND rating IS NOT NULL ORDER BY rating DESC ; name, mediatype, ID, genres, rating
        pair[1].execute(f"SELECT genres FROM media WHERE ID = '{media_id}';") # AND genres is not null
        genre_list = pair[1].fetchall()
        if genre_list[0][0] is None:
            pair[1].execute(f"SELECT ID FROM media WHERE mediaType = '{mediaType}' ORDER BY rating DESC LIMIT '{num}';")
        else:
            genre_items = genre_list[0][0].split(", ")
            genre = genre_items[randint(0, len(genre_items) - 1)]

            pair[1].execute(f"SELECT ID FROM media WHERE mediaType = '{mediaType}' AND genres LIKE '%{genre}%' LIMIT '{num}';")
            
        db_tuples = pair[1].fetchall()
        default_list = []
        for item in db_tuples:
            default_list.append(item[0])

        return default_list

    return "Unexpected error has occurred"       


def get_user_likes(pair, user_id, media_id):
    pair[1].execute("SELECT user_id, media_id, liked FROM preferences;")
    # check if table has values or not
    table = pair[1].fetchall()
    table = [(a, b, int(c)) for a,b,c in table]

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "liked"])
    df2 = df.pivot_table(index=['user_id'], columns=['media_id'], values='liked', fill_value=0)

    transpose = df2.T

    SVD = TruncatedSVD(n_components=3, n_iter=3, random_state=8)

    resultant_matrix = SVD.fit_transform(transpose)
    corr_matrix = np.corrcoef(resultant_matrix)

    col_idx = df2.columns.get_loc("0068646")
    corr_specific = corr_matrix[col_idx]

    df3 = pd.DataFrame({'corr_specific':corr_specific, 'media_id': df2.columns}).sort_values('corr_specific', ascending=False).head(10)


# test cases to test
db = database.open_DBConnection()
#get_user_ratings(db, "3", "0068646", "Movie")
get_user_ratings(db, "3", "9999", "Movie")
get_user_ratings(db, "3", "018DZPUwfDKVrm0IXAP9YM", "Music")
#get_user_ratings(db, "3", "3")
