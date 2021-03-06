import pandas as pd
import numpy as np
import database
import sklearn
from sklearn.decomposition import TruncatedSVD
from random import randint

# add randomness element?
# Based on items you have liked, watched, rated
# Movielens dataset
# Calculate SVD and then use pearson


# removes media_id used for recommendations
def remove_duplicate_media(media_list, media_id):
    if media_id in media_list:
        media_list.remove(media_id)
    else:
        media_list.pop()


# ratings cannot be 0 or function has divide by zero warning
# media_id: media id to compare; num: number of recommendations to return
def get_user_ratings(pair, media_id, mediaType='Movie', num=15):
    pair[1].execute("SELECT user_id, media_id, rating, watched, liked FROM preferences WHERE media_id IN (SELECT ID FROM media WHERE mediaType = %s);", (mediaType,))

    table = pair[1].fetchall()
    table = [(a, b, float(float(c)+2*int(d)+3*int(e))) for a, b, c, d, e in table]

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating"])

    # pivot the table togethers
    rating_table = df.pivot_table(values='rating', index='user_id', columns='media_id', fill_value=0)

    # transpose the pivot table of combined movies
    tranpose = rating_table.T

    # calculate singular value decomposition (SVD) and 
    # scale the resulting matrix from the SVD and transpose
    # n_iter=3 (optional code)
    SVD = TruncatedSVD(n_components=2, random_state=5)
    resultant_matrix = SVD.fit_transform(tranpose)

    # returns the pearson product-moment correlation coefficients
    corr_matrix = np.corrcoef(resultant_matrix)

    # get correlations for recommendations
    try:
        col_index = rating_table.columns.get_loc(media_id)
        corr_specific = corr_matrix[col_index]

        rt = pd.DataFrame({'corr_specific':corr_specific, 'Media': rating_table.columns}).sort_values('corr_specific', ascending=False).head(num + 1)
        recommended_movies = rt['Movies'].tolist()
        remove_duplicate_media(recommended_movies, media_id)

        return recommended_movies

    except KeyError:    # if no recommendations, default recommendations based on genre
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


# test cases to test
#db = database.open_DBConnection()
#l1 = database.get_by_id(db, "12361974")
#print(l1)
#get_user_ratings(db, "3", "0068646", "Movie")
#get_user_ratings(db, "12361974", "Movie")
#get_user_ratings(db, "9999", "Movie")
#get_user_ratings(db, "3", "018DZPUwfDKVrm0IXAP9YM", "Music")
