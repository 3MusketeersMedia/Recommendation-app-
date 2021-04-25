import pandas as pd
import numpy as np
import random
random.seed(0)

def get_user_recommendations(pair, user_id):
    conn[1].execute("SELECT user_id, media_id, rating FROM preferences;")
    table = conn[1].fetchall()

    table = [(a, b, int(c)) for a,b,c in table] 

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating"])
    allRatings = df.pivot_table(index=['user_id'], columns=['media_id'], values='rating')
    print(allRatings.head())

    df = []
    for i in table:
        if i[0] == user_id:
            #get recs by rating
            ratings = allRatings[i[1]]
            similarMovies = allRatings.corrwith(ratings)
            similarMovies = similarMovies.dropna()

            similarMovies = pd.DataFrame(similarMovies.sort_values(ascending=False))
            similarMovies = list(similarMovies.itertuples(index=True, name=None))
            
            if len(similarMovies) > 0:
                df = df + similarMovies

    #store, media_id and correlation score
    #return list of media_id
    df = sorted(df, key = lambda x: x[1], reverse=True)
    print(df)
    return [i[0] for i in df]

#load file
exec(open("../database/database.py").read())

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
