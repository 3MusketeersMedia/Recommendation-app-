import psycopg2
import psycopg2.extras
#----------Setup----------------------
#verify connection
#setup database
conn = psycopg2.connect(host="mediadb.c3txk3dmci6e.us-west-1.rds.amazonaws.com", port="5432", user='postgres', password='postgres')
conn.autocommit = True #autocommit or commit after transactions
database = conn.cursor()

if conn is None:
    print("Failed to Connect to DB")
    exit()

#make tables
database.execute("CREATE TABLE IF NOT EXISTS media(name VARCHAR NOT NULL, mediaType VARCHAR NOT NULL, year INT, link VARCHAR, genres VARCHAR, rating NUMERIC, running_time NUMERIC, summary VARCHAR, ID VARCHAR, PRIMARY KEY(ID));")

database.execute("CREATE TABLE IF NOT EXISTS users(username VARCHAR NOT NULL, password_hash VARCHAR NOT NULL, password_salt VARCHAR NOT NULL, ID VARCHAR, PRIMARY KEY(ID));")

conn.close()

#-------------Setup End----------------


#-----------Function Definitions------------
def open_DBConnection(dict_cursor=False):
    connection = psycopg2.connect(host="mediadb.c3txk3dmci6e.us-west-1.rds.amazonaws.com", port="5432", user='postgres', password='postgres')
    connection.autocommit = True
    if dict_cursor == True:
        db = connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
    else:
        db = connection.cursor()
    return (connection, db, dict_cursor)


def close_DBConnection(pair):
    pair[0].close()


def add_user(pair, username, password_hash, password_salt, user_id):
    pair[1].execute("SELECT ID FROM users WHERE ID = '{}';".format(user_id))
    list_id = pair[1].fetchall()

    if pair[2] == False:
        if (user_id,) in list_id:
            pair[1].execute("UPDATE users SET username = '{}', password_hash = '{}', password_salt = '{}' WHERE ID = '{}';".format(username, password_hash, password_salt, user_id))
            #update if true
        else:
            pair[1].execute("INSERT INTO users VALUES('{}', '{}', '{}', '{}');".format(username, password_hash, password_salt, user_id))
            #insert if false
    else:
        if len(list_id) > 0 and user_id == list_id[0]['id']:
            pair[1].execute("UPDATE users SET username = '{}', password_hash = '{}', password_salt = '{}' WHERE ID = '{}';".format(username, password_hash, password_salt, user_id))
            #update if true
        else:
            pair[1].execute("INSERT INTO users VALUES('{}', '{}', '{}', '{}');".format(username, password_hash, password_salt, user_id))
            #insert if false


def set_data(pair, name, mediaType, year, link, genres, rating, running_time, ID, summary="None"):
    #retrieve list of ID's
    pair[1].execute("SELECT ID FROM media WHERE ID = '{}';".format(ID))
    list_id = pair[1].fetchall()
    #check for ID
    if pair[2] == False:
        if (ID,) in list_id:
            pair[1].execute("UPDATE media SET name = '{}', mediaType = '{}', year = {}, link = '{}', genres = '{}', rating = {}, running_time = {}, summary = '{}' WHERE ID = '{}';".format(name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #update if true
        else:
            pair[1].execute("INSERT INTO media VALUES('{}', '{}', {}, '{}', '{}', {}, {}, '{}', '{}');".format(name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #insert if false
    else:
        if len(list_id) > 0 and ID == list_id[0]['id']:
            pair[1].execute("UPDATE media SET name = '{}', mediaType = '{}', year = {}, link = '{}', genres = '{}', rating = {}, running_time = {}, summary = '{}' WHERE ID = '{}';".format(name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #update if true
        else:
            pair[1].execute("INSERT INTO media VALUES('{}', '{}', {}, '{}', '{}', {}, {}, '{}', '{}');".format(name, mediaType, year, link, genres, rating, running_time, summary, ID))
            #insert if false


def set_user_data(pair, table, watched, liked, ID, rating="NULL", review=" "):
    #retrieve list of ID's
    pair[1].execute("SELECT ID FROM {} WHERE ID = '{}';".format(table, ID))
    list_id = pair[1].fetchall()
    #check for ID
    if pair[2] == False:
        if (ID,) in list_id:
            pair[1].execute("UPDATE {} SET watched = {}, liked = {}, rating = {}, review = '{}' WHERE ID = '{}';".format(table, watched, liked, rating, review, ID))
            #update if true
        else:
            pair[1].execute("INSERT INTO {} VALUES({}, {}, {}, '{}', '{}');".format(table, watched, liked, rating, review, ID))
            #insert if false
    else:
        if len(list_id) > 0 and ID == list_id[0]['id']:
            pair[1].execute("UPDATE {} SET watched = {}, liked = {}, rating = {}, review = '{}' WHERE ID = '{}';".format(table, watched, liked, rating, review, ID))
            #update if true
        else:
            pair[1].execute("INSERT INTO {} VALUES({}, {}, {}, '{}', '{}');".format(table, watched, liked, rating, review, ID))
            #insert if false



def set_data_liked(pair, ID, user, liked=True):
    pair[1].execute("UPDATE {} SET liked = {} WHERE ID = '{}';".format(user, liked, ID))


def set_data_watched(pair, ID, user, watched=True):
    pair[1].execute("UPDATE {} SET watched = {} WHERE ID = '{}';".format(user, watched, ID))


def set_data_id(pair, oldID, newID, table="media"):
    pair[1].execute("UPDATE {} SET ID = '{}' WHERE ID = '{}';".format(table, newID, oldID))


def get_by_name(pair, name):
    pair[1].execute("SELECT * FROM media WHERE name = '{}';".format(name))
    return pair[1].fetchall()


def get_by_id(pair, ID, table="media"):
    #check if ID exists
    pair[1].execute("SELECT ID FROM {} WHERE ID = '{}';".format(table, ID))
    list_id = pair[1].fetchall()
    if pair[2] == False:
        if (ID,) in list_id:
            pair[1].execute("SELECT * FROM {} WHERE ID = '{}';".format(table, ID))
            return pair[1].fetchone()
        else:
            return None
    else:
        if len(list_id) > 0 and ID == list_id[0]['id']:
            pair[1].execute("SELECT * FROM {} WHERE ID = '{}';".format(table, ID))
            return pair[1].fetchone()
        else:
            return None


def get_by_liked(pair, table, liked=True):
    pair[1].execute("SELECT * FROM {} WHERE liked = {};".format(table, liked))
    return pair[1].fetchall()


def get_by_watched(pair, table, watched=True):
    pair[1].execute("SELECT * FROM {} WHERE watched = {};".format(table, watched))
    return pair[1].fetchall()


def get_by_genre(pair, genre):
    pair[1].execute("SELECT * FROM media WHERE POSITION('{}' in genres) > 0;".format(genre))
    return pair[1].fetchall()


def get_all(pair, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].fetchall()


def get_next(pair):
    return pair[1].fetchall()


def get_by_mediaType(pair, mediaType):
    pair[1].execute("SELECT * FROM media WHERE mediaType = '{}';".format(mediaType))
    return pair[1].fetchall() 


def get_by_year(pair, start, end=-1):
    if(end == -1):
        end = start
    pair[1].execute("SELECT * FROM media WHERE year >= {} AND year <= {};".format(start, end))
    return pair[1].fetchall()


def get_by_rating(pair, start, end=-1):
    if(end == -1):
        end = start
    pair[1].execute("SELECT * FROM media WHERE rating >= {} AND rating <= {};".format(start, end))
    return pair[1].fetchall()


def get_by_running_time(pair, start, end=-1):
    if(end == -1):
        end = start
    pair[1].execute("SELECT * FROM media WHERE running_time >= {} AND running_time <= {};".format(start, end))
    return pair[1].fetchall()


def delete_data(pair, ID, table="media"):
    pair[1].execute("DELETE FROM {} WHERE ID = '{}';".format(table, ID))


def delete_table(pair, table):
    pair[1].execute("DROP TABLE {} CASCADE;".format(table))


def create_user_table(pair, user):
    pair[1].execute("CREATE TABLE IF NOT EXISTS {}(watched BOOLEAN NOT NULL, liked BOOLEAN NOT NULL, rating NUMERIC, review VARCHAR, ID VARCHAR, FOREIGN KEY (ID) REFERENCES media (ID));".format(user))


def clear_data(pair, table):
    pair[1].execute("DELETE FROM {};".format(table))


def num_items(pair, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].rowcount

#-------------------Function Defintion End------------------------
