import pandas as pd
import numpy as np
import random
import database

def get_user_likes(pair, user_id):

    pair[1].execute("SELECT user_id, media_id, liked FROM preferences;")
    table = pair[1].fetchall()

    table = [(a, b, int(c)) for a,b,c in table] 

    #list of all ratings
    df = pd.DataFrame(table, columns=["user_id", "media_id", "rating"])
    print(df)

def get_user_watched(pair, user_id):
    pass


# main execution for testing
db = database.open_DBConnection()
#list_movies = database.get_all(db)

get_user_likes(db, "3")
