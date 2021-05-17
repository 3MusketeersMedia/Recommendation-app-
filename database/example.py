
#python3 and up
exec(open("database.py").read())

#below python3 
#execfile("database.py")

#establish connection
connection = open_DBConnection()
conn = connection
#print(advanced_search_media_table(connection, 'El Tango del Viudo y Su Espejo Deformante', 'movie', 'Drama', 1800, 0, 2050, 10))
print(num_items(connection))

list_movies = get_all(connection)

#add a bunch of users
add_user(conn, "username1", "password_salt")
add_user(conn, "username2", "password_salt")
add_user(conn, "username3", "password_salt")
add_user(conn, "username4", "password_salt")
add_user(conn, "username5", "password_salt")
random.seed(0)
#set a bunch of user preferences
ids = [str(get_user_id(conn, "username1")), str(get_user_id(conn, "username2")), str(get_user_id(conn, "username3")), str(get_user_id(conn, "username4")), str(get_user_id(conn, "username5"))]

z = 5 
for i in ids:
    for x in range(z):
        set_preference(conn, bool(random.randint(0,1)), bool(random.randint(0, 1)), i, list_movies[x][8], rating=random.randint(0, 10))
    z+=1

set_preference(conn, True, True, str(get_user_id(conn, "username5")), list_movies[20][8], rating=10)
set_preference(conn, True, True, str(get_user_id(conn, "username4")), list_movies[20][8], rating=10)
#get movie_id, user_id and rating and name
print(get_user_recommendations(conn, str(get_user_id(conn, "username5"))))

clear_data(conn, "preferences")
clear_data(conn, "users")

#add_user(connection, "user", "salt")
#i = get_user_id(connection, "user")
#add_user_pic(connection, i, 'IMG_1795.png')
#get_user_pic(connection, i)
#clear_table(connection, "users")

#print(search_media_table(connection, 'El Tango del Viudo y Su Espejo Deformante'))
#set_data(connection, "b show", "tv show", 1999, "urlinhere", "horror thriller action", 10.19, 100.5, "1")
#set_data(connection, "p show", "tv show", 1999, "urlinhere", "horror thriller", 10.17, 100.6, "2")
#set_data(connection, "m movie", "movie", 1999, "urlinhere", "horror thriller", 10.17, 100.5, "3")
#set_data(connection, "x movie", "movie", 1999, "urlinhere", "horror thriller", 10.17, 100.7, "4")
#set_data(connection, "y movie", "movie", 1999, "urlinhere", "horror thriller action", 10.18, 100.5, "5")

#print(get_by_mediaType(connection, "movie"))
#print(get_by_year(connection, 1998))
#print(get_by_rating(connection, 10.18, 10.21))
#print(get_by_running_time(connection, 100.6, 100.7))

#create_user_table(connection, "jane_goodall")

#set_user_data(connection, "jane_goodall", False, False, "1", 10.17)
#set_user_data(connection, "jane_goodall", True, False, "2")
#set_user_data(connection, "jane_goodall", False, True, "3")
#set_user_data(connection, "jane_goodall", True, True, "4")
#set_user_data(connection, "jane_goodall", False, False, "5")
#add_user(connection, "namehere", "string", "string", "1")
#add_user(connection, "namehere", "string", "string", "2")
#add_user(connection, "namehere", "string", "string", "3")
#print(get_all(connection, "users"))

#print(get_by_id(connection, "7"))
#print(get_by_id(connection, "1", "jane_goodall"))
#print(get_by_id(connection, "1", "users"))

#print(num_items(connection, "jane_goodall"))
#print(num_items(connection))

#print(get_all(connection))
#print(get_all(connection, "jane_goodall"))
#print(get_by_genre(connection, "action"))

close_DBConnection(connection)
