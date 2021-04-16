
#python3 and up
exec(open("database.py").read())

#below python3 
#execfile("database.py")

#establish connection
connection = open_DBConnection()

set_data(connection, "v show", "tv show", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "0")
set_data(connection, "b show", "tv show", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "1")
set_data(connection, "p show", "tv show", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "2")
set_data(connection, "m movie", "movie", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "3")
set_data(connection, "x movie", "movie", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "4")
set_data(connection, "y movie", "movie", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "5")

print(get_by_mediaType(connection, "movie"))

create_user_table(connection, "jane_goodall")

set_user_data(connection, "jane_goodall", False, False, "1")
set_user_data(connection, "jane_goodall", True, False, "2")
set_user_data(connection, "jane_goodall", False, True, "3")
set_user_data(connection, "jane_goodall", True, True, "4")
set_user_data(connection, "jane_goodall", False, False, "5")

print(get_by_id(connection, 1))
print(get_by_id(connection, 1, "jane_goodall"))

print(num_items(connection, "jane_goodall"))
print(num_items(connection))

print(get_all(connection, "jane_goodall"))

close_DBConnection(connection)
