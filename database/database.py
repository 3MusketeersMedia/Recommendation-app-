import psycopg2

#postgres sql installation
#--------------------------------------
#sudo apt install python2
#curl https://bootstrap.pypa.io/pip/2.7/get-pip.py --output get-pip.py
#sudo python2 get-pip.py
#pip2 install psycopg2
#run with python2.7
#-------------------------------------

#example of how to use file in a sample python doc
#-------------------------------------
#import statements
#
#execfile("location/database.py")
#connection = open_DBConnection()
#
#interact with data here
#
#close_DBConnection(connection)
#-------------------------------------


#----------Setup----------------------
#verify connection
#setup database
conn = psycopg2.connect(dbname = "postgres")
conn.autocommit = True #autocommit or commit after transactions
database = conn.cursor()

if conn is not None:
    database.execute("SELECT datname FROM pg_database;")
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
#openDBConnection() -> open connection to db
#close_DBConnection(pair) -> close connection to db
#set_data(pair, name, mediaType, ID) -> set entry or insert new entry into table
#set_data_id(pair, ID) -> set id of existing data point
#get_by_name(pair, name) -> get all entries of a given name
#get_by_id(pair, ID) -> get entry by ID
#get_by_mediaType(pair, mediaType) -> get entry by mediaType
#delete_data(pair, ID) -> delete a data point
#clear(pair) -> clear table

#Constraints:
#   none
#Parameters:
#   none
#Return Type:
#   pair-> a tuple with (connection, database) store this value for other functions when interacting with db
def open_DBConnection():
    connection = psycopg2.connect(dbname = "maindb")
    connection.autocommit = True
    db = connection.cursor()
    return (connection, db)


#Constraints:
#   database must be open first
#Parameters:
#   pair->tuple from open_DBConnection()
#Return Type:
#   none
def close_DBConnection(pair):
    pair[0].close()


#Constraints:
#   Cannot reset ID
#   ID MUST BE UNIQUE, everthing else can have duplicates
#Parameters:
#   pair -> (connection, database) tuple from open_DBConnection()
#   name -> string
#   mediaType -> The following strings: 'movie', 'tv show', 'short film', 'anime', or 'manga'
#   ID -> integer
#Return Type:
#   none
def set_data(pair, name, mediaType, ID):
    #retrieve list of ID's
    pair[1].execute("SELECT ID FROM media;")
    list_id = pair[1].fetchall()
    #check for ID
    if (ID,) in list_id:
        pair[1].execute("UPDATE media SET name = '{}', mediaType = '{}' WHERE ID = {};".format(name, mediaType, ID))
        #update if true
    else:
        pair[1].execute("INSERT INTO media VALUES('{}', '{}', {});".format(name, mediaType, ID))
        #insert if false


#Constraints:
#   All ID's must be unique
#   If ID is the same as an existing ID, the other parameters will be updated
#Paremeters:
#   pair -> tuple from open_DBConnection()
#   oldID -> int
#   newID -> int
#Return Type:
#   none
def set_data_id(pair, oldID, newID):
    pair[1].execute("SELECT ID FROM media;")
    list_id = pair[1].fetchall()
    if (oldID,) in list_id:
        pair[1].execute("UPDATE media SET ID = '{}' WHERE ID = {};".format(newID, oldID))


#Constraints:
#   none
#Paremeters:
#   pair -> tuple from open_DBConnection()
#   name -> string
#Return Type:
#   list of tuples -> list of (name, mediaType, ID)
def get_by_name(pair, name):
    pair[1].execute("SELECT name, mediaType, ID FROM media WHERE name = '{}'".format(name))
    return pair[1].fetchall()


#Constraints:
#   none
#Paremeters:
#   pair -> tuple from open_DBConnection()
#   ID -> int
#Return Type:
#   tuple -> (name, mediaType, ID)
def get_by_id(pair, ID):
    pair[1].execute("SELECT name, mediaType, ID FROM media WHERE ID = {}".format(ID))
    value = pair[1].fetchall()
    return tuple((value[0][0], value[0][1], value[0][2]))


#Constraints:
#   none
#Paremeters:
#   pair -> tuple from open_DBConnection()
#   mediaType -> string
#Return Type:
#   list of tuples -> list of (name, mediaType, ID)
def get_by_mediaType(pair, mediaType):
    pair[1].execute("SELECT name, mediaType, ID FROM media WHERE mediaType = '{}'".format(mediaType))
    return pair[1].fetchall() 


#Constraints:
#   Must Exist
#Paremeters:
#   pair -> tuple from open_DBConnection
#   ID -> int
#Return Type:
#   none
def delete_data(pair, ID):
    pair[1].execute("DELETE FROM media WHERE ID = {};".format(ID))


#Constraints:
#   none
#Paremeters:
#   pair -> tuple from open_DBConnection
#Return Type:
#   none
def clear_data(pair):
    pair[1].execute("DELETE FROM media;")

