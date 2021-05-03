import psycopg2
import psycopg2.extras
from model import *
#----------Setup----------------------
#verify connection
#setup database
conn = psycopg2.connect(host="mediadb.c3txk3dmci6e.us-west-1.rds.amazonaws.com", port="5432", user='postgres', password='postgres', dbname='db')
conn.autocommit = True #autocommit or commit after transactions
database = conn.cursor()

if conn is None:
    print("Failed to Connect to DB")
    exit()

#make tables
database.execute("CREATE TABLE IF NOT EXISTS media(name VARCHAR NOT NULL, mediaType VARCHAR NOT NULL, year INT, link VARCHAR, genres VARCHAR, rating NUMERIC, running_time NUMERIC, summary VARCHAR, ID VARCHAR, PRIMARY KEY(ID));")

database.execute("CREATE TABLE IF NOT EXISTS users(username VARCHAR NOT NULL UNIQUE, password_hash VARCHAR NOT NULL, password_salt VARCHAR NOT NULL, ID VARCHAR, PRIMARY KEY(ID));")

database.execute("CREATE TABLE IF NOT EXISTS preferences(watched BOOLEAN NOT NULL, liked BOOLEAN NOT NULL, rating NUMERIC, review VARCHAR, user_id VARCHAR, media_id VARCHAR, FOREIGN KEY (user_id) REFERENCES users (ID), FOREIGN KEY (media_id) REFERENCES media (ID));")

conn.close()

#-------------Setup End----------------


#-----------Function Definitions------------
def open_DBConnection(dict_cursor=False):
    connection = psycopg2.connect(host="mediadb.c3txk3dmci6e.us-west-1.rds.amazonaws.com", port="5432", user='postgres', password='postgres', dbname='db')
    connection.autocommit = True
    if dict_cursor == True:
        db = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        db = connection.cursor()
    return (connection, db, dict_cursor)


def close_DBConnection(pair):
    pair[0].close()

def advanced_search(pair, genre, minYear, maxYear, minRate, maxRate):
    # First, some edge case handling (based on user input)
    if maxYear == "":
        if minYear == "":
            minYear = "1500"
            maxYear = "2050"
        else:
            maxYear = minYear
    if maxRate == "":
        if minRate == "":
            minRate = 0
            maxRate = 5
        else:
            maxRate = minRate
    # Since genre can't be generalized like the params, above, must have two possible queries
    if genre != "":
        pair[1].execute("SELECT * FROM media WHERE POSITION(%s in genres) > 0 AND year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (genre, minYear, maxYear, minRate, maxRate))
    else:
        pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s AND rating >= %s AND rating <= %s;", (minYear, maxYear, minRate, maxRate))
    return pair[1].fetchall()

def add_user(pair, username, password_hash, password_salt):
    pair[1].execute("SELECT username FROM users WHERE username = %s;", (username,))
    list_id = pair[1].fetchall()
    user_id = str(hash(username))

    if pair[2] == False:
        if (username,) in list_id:
            pair[1].execute("UPDATE users SET username = %s, password_hash = %s, password_salt = %s WHERE ID = %s;", (username, password_hash, password_salt, user_id))
            #update if true
        else:
            pair[1].execute("INSERT INTO users VALUES(%s, %s, %s, %s);", (username, password_hash, password_salt, user_id))
            #insert if false
    else:
        if len(list_id) > 0 and username == list_id[0]['username']:
            pair[1].execute("UPDATE users SET username = %s, password_hash = %s, password_salt = %s WHERE ID = %s;", (username, password_hash, password_salt, user_id))
            #update if true
        else:
            pair[1].execute("INSERT INTO users VALUES(%s, %s, %s, %s);", (username, password_hash, password_salt, user_id))
            #insert if false


def check_user_exists(pair, username):
    pair[1].execute("SELECT username FROM users WHERE username = %s", (username,))
    list_id = pair[1].fetchall()
    if (username,) in list_id:
        return True
    else:
        return False


def get_user_id(pair, username):
    pair[1].execute("SELECT ID FROM users WHERE username = %s", (username,))
    return pair[1].fetchone()


def set_data(pair, name, mediaType, year, link, genres, rating, running_time, ID, summary="None"):
    #retrieve list of ID's
    pair[1].execute("SELECT ID FROM media WHERE ID = %s;", (ID,))
    list_id = pair[1].fetchall()
    #check for ID
    if pair[2] == False:
        if (ID,) in list_id:
            pair[1].execute("UPDATE media SET name = %s, mediaType = %s, year = %s, link = %s, genres = %s, rating = %s, running_time = %s, summary = %s WHERE ID = %s;", (name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #update if true
        else:
            pair[1].execute("INSERT INTO media VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);", (name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #insert if false
    else:
        if len(list_id) > 0 and ID == list_id[0]['id']:
            pair[1].execute("UPDATE media SET name = %s, mediaType = %s, year = %s, link = %s, genres = %s, rating = %s, running_time = %s, summary = %s WHERE ID = %s;", (name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #update if true
        else:
            pair[1].execute("INSERT INTO media VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);", (name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #insert if false


def set_preference(pair, watched, liked, user_id, media_id, rating=0, review=" "):
    pair[1].execute("SELECT user_id, media_id FROM preferences WHERE user_id = %s AND media_id = %s;", (user_id, media_id))
    list_id = pair[1].fetchall()

    if pair[2] == False:
        if (user_id, media_id) in list_id:
            pair[1].execute("UPDATE preferences SET watched = %s, liked = %s, rating = %s, review = %s WHERE user_id = %s AND media_id = %s;", (watched, liked, rating, review, user_id, media_id))
            #update if true
        else:
            pair[1].execute("INSERT INTO preferences VALUES(%s, %s, %s, %s, %s, %s);", (watched, liked, rating, review, user_id, media_id))
            #insert if false
    else:
        if len(list_id) > 0 and user_id == list_id[0]['user_id'] and media_id == list_id[0]['media_id']:
            pair[1].execute("UPDATE preferences SET watched = %s, liked = %s, rating = %s, review = %s WHERE user_id = %s AND media_id = %s;", (watched, liked, rating, review, user_id, media_id))
            #update if true
        else:
            pair[1].execute("INSERT INTO preferences VALUES(%s, %s, %s, %s, %s, %s);", (watched, liked, rating, review, user_id, media_id))
            #insert if false


def set_data_liked(pair, user_id, media_id, liked=True):
    pair[1].execute("UPDATE preferences SET liked = %s WHERE user_id = %s AND media_id = %s;", (liked, user_id, media_id))


def set_data_watched(pair, user_id, media_id, watched=True):
    pair[1].execute("UPDATE preferences SET watched = %s WHERE user_id = %s AND media_id = %s;", (watched, user_id, media_id))


def set_data_id(pair, oldID, newID, table="media"):
    pair[1].execute("UPDATE {} SET ID = %s WHERE ID = %s;".format(table), (newID, oldID))


def get_user_preferences(pair, user_id):
    pair[1].execute("SELECT * FROM preferences WHERE user_id = %s;", (user_id,))
    return pair[1].fetchall()


def get_user_preference(pair, user_id, media_id):
    pair[1].execute("SELECT * FROM preferences WHERE user_id = %s AND media_id = %s;", (user_id, media_id))
    return pair[1].fetchall()


def get_user_liked(pair, user_id, liked=True):
    pair[1].execute("SELECT * FROM preferences WHERE user_id = %s AND liked = %s;", (user_id, liked))
    return pair[1].fetchall()


def get_user_watched(pair, user_id, watched=True):
    pair[1].execute("SELECT * FROM preferences WHERE user_id = %s AND watched = %s;", (user_id, watched))
    return pair[1].fetchall()


def get_by_name(pair, name):
    pair[1].execute("SELECT * FROM media WHERE name = %s;", (name,))
    return pair[1].fetchall()


def get_by_id(pair, ID, table="media"):
    #check if ID exists
    pair[1].execute("SELECT ID FROM {} WHERE ID = %s;".format(table), (ID,))
    list_id = pair[1].fetchall()
    if pair[2] == False:
        if (ID,) in list_id:
            pair[1].execute("SELECT * FROM {} WHERE ID = %s;".format(table), (ID,))
            return pair[1].fetchone()
        else:
            return None
    else:
        if len(list_id) > 0 and ID == list_id[0]['id']:
            pair[1].execute("SELECT * FROM {} WHERE ID = %s;".format(table), (ID,))
            return pair[1].fetchone()
        else:
            return None


def get_by_liked(pair, liked=True):
    pair[1].execute("SELECT * FROM preferences WHERE liked = %s;", (liked,))
    return pair[1].fetchall()


def get_by_watched(pair, watched=True):
    pair[1].execute("SELECT * FROM preferences WHERE watched = %s;", (watched,))
    return pair[1].fetchall()


def get_by_genre(pair, genre):
    pair[1].execute("SELECT * FROM media WHERE POSITION(%s in genres) > 0;", (genre,))
    return pair[1].fetchall()


def get_many(pair, limit, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].fetchmany(limit)


def get_all(pair, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].fetchall()


def get_next(pair):
    return pair[1].fetchall()


def get_by_mediaType(pair, mediaType):
    pair[1].execute("SELECT * FROM media WHERE mediaType = %s;", (mediaType,))
    return pair[1].fetchall() 


def get_by_year(pair, start, end=-1):
    if(end == -1):
        end = start
    pair[1].execute("SELECT * FROM media WHERE year >= %s AND year <= %s;", (start, end))
    return pair[1].fetchall()


def get_by_rating(pair, start, end=-1):
    if(end == -1):
        end = start
    pair[1].execute("SELECT * FROM media WHERE rating >= %s AND rating <= %s;", (start, end))
    return pair[1].fetchall()


def get_by_running_time(pair, start, end=-1):
    if(end == -1):
        end = start
    pair[1].execute("SELECT * FROM media WHERE running_time >= %s AND running_time <= %s;", (start, end))
    return pair[1].fetchall()


def delete_data(pair, ID, table="media"):
    pair[1].execute("DELETE FROM {} WHERE ID = %s;".format(table), (ID,))


def delete_preference(pair, user_id, media_id):
    pair[1].execute("DELETE FROM preferences WHERE user_id = %s AND media_id = %s;", (user_id, media_id))


def delete_table(pair, table):
    pair[1].execute("DROP TABLE {} CASCADE;".format(table))


def clear_data(pair, table):
    pair[1].execute("DELETE FROM {};".format(table))


def num_items(pair, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].rowcount

#-------------------Function Defintion End------------------------
