import pandas as pd
import numpy as np
import random

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

'''
#load file
exec(open("backend/database.py").read())
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

'''
