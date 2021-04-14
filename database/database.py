import psycopg2

#----------Setup----------------------
#verify connection
#setup database
conn = psycopg2.connect(host="mediadb.c3txk3dmci6e.us-west-1.rds.amazonaws.com", port="5432", user="postgres", password="postgres")
conn.autocommit = True #autocommit or commit after transactions
database = conn.cursor()

if conn is None:
    print("Failed to Connect to DB")
    exit()

#make tables
database.execute("CREATE TABLE IF NOT EXISTS media(name VARCHAR (50) NOT NULL, mediaType VARCHAR (50) NOT NULL, ID INT PRIMARY KEY, CHECK (mediaType = 'movie' OR mediaType = 'tv show' OR mediaType = 'short film' OR mediaType = 'anime' OR mediaType = 'manga'));")

conn.close()

#-------------Setup End----------------


#-----------Function Definitions------------
def open_DBConnection():
    connection = psycopg2.connect(host="mediadb.c3txk3dmci6e.us-west-1.rds.amazonaws.com", port="5432", user="postgres", password="postgres")
    connection.autocommit = True
    db = connection.cursor()
    return (connection, db)


def close_DBConnection(pair):
    pair[0].close()


def set_data(pair, name, mediaType, ID):
    #retrieve list of ID's
    pair[1].execute("SELECT ID FROM media WHERE ID = {};".format(ID))
    list_id = pair[1].fetchall()
    #check for ID
    if (ID,) in list_id:
        pair[1].execute("UPDATE media SET name = '{}', mediaType = '{}' WHERE ID = {};".format(name, mediaType, ID))
        #update if true
    else:
        pair[1].execute("INSERT INTO media VALUES('{}', '{}', {});".format(name, mediaType, ID))
        #insert if false


def set_user_data(pair, table, watched, liked, ID):
    #retrieve list of ID's
    pair[1].execute("SELECT ID FROM {} WHERE ID = {};".format(table, ID))
    list_id = pair[1].fetchall()
    #check for ID
    if (ID,) in list_id:
        pair[1].execute("UPDATE {} SET watched = {}, liked = {} WHERE ID = {};".format(table, watched, liked, ID))
        #update if true
    else:
        pair[1].execute("INSERT INTO {} VALUES({}, {}, {});".format(table, watched, liked, ID))
        #insert if false


def set_data_liked(pair, ID, user, liked=True):
    pair[1].execute("UPDATE {} SET liked = {} WHERE ID = {};".format(user, liked, ID))


def set_data_watched(pair, ID, user, watched=True):
    pair[1].execute("UPDATE {} SET watched = {} WHERE ID = {};".format(user, watched, ID))


def set_data_id(pair, oldID, newID, table="media"):
    pair[1].execute("UPDATE {} SET ID = '{}' WHERE ID = {`};".format(table, newID, oldID))


def get_by_name(pair, name):
    pair[1].execute("SELECT * FROM media WHERE name = '{}';".format(name))
    return pair[1].fetchall()


def get_by_id(pair, ID, table="media"):
    #check if ID exists
    pair[1].execute("SELECT ID FROM {} WHERE ID = {};".format(table, ID))
    list_id = pair[1].fetchall()
    if (ID,) in list_id:
        pair[1].execute("SELECT * FROM {} WHERE ID = {};".format(table, ID))
        value = pair[1].fetchall()
        return tuple((value[0][0], value[0][1], value[0][2]))
    else:
        return None


def get_by_liked(pair, table, liked=True):
    pair[1].execute("SELECT * FROM {} WHERE liked = {}".format(table, liked))
    return pair[1].fetchall()


def get_by_watched(pair, table, watched=True):
    pair[1].execute("SELECT * FROM {} WHERE watched = {}".format(table, watched))
    return pair[1].fetchall()


def get_all(pair, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].fetchall()


def get_next(pair):
    return pair[1].fetchall()


def get_by_mediaType(pair, mediaType):
    pair[1].execute("SELECT * FROM media WHERE mediaType = '{}';".format(mediaType))
    return pair[1].fetchall() 


def delete_data(pair, ID, table="media"):
    pair[1].execute("DELETE FROM {} WHERE ID = {};".format(table, ID))


def delete_table(pair, table):
    pair[1].execute("DROP TABLE {} CASCADE;".format(table))


def create_user_table(pair, user):
    pair[1].execute("CREATE TABLE IF NOT EXISTS {}(watched BOOLEAN NOT NULL, liked BOOLEAN NOT NULL, ID INT PRIMARY KEY);".format(user))


def clear_data(pair, table):
    pair[1].execute("DELETE FROM {};".format(table))


def num_items(pair, table="media"):
    pair[1].execute("SELECT * FROM {};".format(table))
    return pair[1].rowcount

#-------------------Function Defintion End------------------------
