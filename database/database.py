import psycopg2

#----------Setup----------------------
#verify connection
#setup database
conn = psycopg2.connect(dbname = "postgres")
conn.autocommit = True #autocommit or commit after transactions
database = conn.cursor()

if conn is not None:
    database.execute("SELECT datname FROM pg_database WHERE datname = '{}';".format("maindb"))
    list_db = database.fetchall()
    
    if ("maindb",) not in list_db:
        database.execute("CREATE DATABASE maindb OWNER postgres;")
else:
    print("Failed to Connect to DB")
    exit()

#close prev connection
conn.close()

#set cursor to newly created maindb
conn = psycopg2.connect(dbname = "maindb")
conn.autocommit = True
database = conn.cursor()

#make tables
database.execute("CREATE TABLE IF NOT EXISTS media(name VARCHAR (50) NOT NULL, mediaType VARCHAR (50) NOT NULL, ID INT PRIMARY KEY, CHECK (mediaType = 'movie' OR mediaType = 'tv show' OR mediaType = 'short film' OR mediaType = 'anime' OR mediaType = 'manga'));")

conn.close()

#-------------Setup End----------------


#-----------Function Definitions------------
def open_DBConnection():
    connection = psycopg2.connect(dbname = "maindb")
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


def set_data_id(pair, oldID, newID):
    pair[1].execute("SELECT ID FROM media WHERE ID = {};".format(oldID))
    list_id = pair[1].fetchall()
    if (oldID,) in list_id:
        pair[1].execute("UPDATE media SET ID = '{}' WHERE ID = {};".format(newID, oldID))


def get_by_name(pair, name):
    pair[1].execute("SELECT name, mediaType, ID FROM media WHERE name = '{}';".format(name))
    return pair[1].fetchall()


def get_by_id(pair, ID):
    #check if ID exists
    pair[1].execute("SELECT ID FROM media WHERE ID = {};".format(ID))
    list_id = pair[1].fetchall()
    if (ID,) in list_id:
        pair[1].execute("SELECT name, mediaType, ID FROM media WHERE ID = {};".format(ID))
        value = pair[1].fetchall()
        return tuple((value[0][0], value[0][1], value[0][2]))
    else:
        return []


def get_next(pair):
    return pair[1].fetchall()


def get_by_mediaType(pair, mediaType):
    pair[1].execute("SELECT name, mediaType, ID FROM media WHERE mediaType = '{}';".format(mediaType))
    return pair[1].fetchall() 


def delete_data(pair, ID):
    pair[1].execute("DELETE FROM media WHERE ID = {};".format(ID))


def clear_data(pair):
    pair[1].execute("DELETE FROM media;")


def num_items(pair):
    pair[1].execute("SELECT * FROM media;")
    return pair[1].rowcount

#-------------------Function Defintion End------------------------
