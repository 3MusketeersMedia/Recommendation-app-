
#python3 and up
exec(open("database.py").read())

#below python3 
#execfile("database.py")

#establish connection
connection = open_DBConnection()

set_data(connection, "vinu show", "tv show", 1)
set_data(connection, "vinu show", "movie", 2)
set_data(connection, "vinu show", "short film", 3)
set_data(connection, "belen show", "movie", 4)
set_data(connection, "booby show", "movie", 5)
set_data(connection, "dooby show", "anime", 6)

stuff = get_by_name(connection, "vinu show")
print(stuff)

stuff = get_by_id(connection, 6)
print(stuff)

stuff = get_by_mediaType(connection, "movie")
print(stuff)

clear_data(connection)
close_DBConnection(connection)
