import time
import random
import decimal
from mal import *
#python3 and up
exec(open("database.py").read())

#below python3 
#execfile("database.py")

#establish connection
conn = open_DBConnection()
#print(advanced_search_media_table(connection, 'El Tango del Viudo y Su Espejo Deformante', 'movie', 'Drama', 1800, 0, 2050, 10))

print(num_items(conn))
list_movies = get_all(conn)
separator = ', '

print("Deleting...")
conn[1].execute("DELETE FROM media WHERE LOWER(genres) LIKE '%ecchi%' OR LOWER(genres) LIKE '%hentai%';")

print("Done. Searching Media Table...")
print(search_media_table(conn, "teh avengrs"))

print("Done. Capitalizing music...")
conn[1].execute("UPDATE media SET mediaType='Music' WHERE mediaType='music';")

print("Done. Capitalizing movie...")
conn[1].execute("UPDATE media SET mediaType='Movie' WHERE mediaType='movie';")

print("Done. Changing genres to be separated by comma...")
conn[1].execute("SELECT ID, genres FROM media WHERE genres LIKE '%|%';")
bar_genres = conn[1].fetchall()
for a,b in bar_genres:
    tempo = b.split("|")
    tempo = separator.join(tempo)
    conn[1].execute("UPDATE media SET genres = %s WHERE ID = %s;", (tempo, a))

#print("Done. Testing user ratings...")
#print(recommend.get_user_ratings(conn, list_movies[0][9]))

#print("Done. Adding Users...")
#for i in range(0, 25):
    #tmp = "user" + str(i)
    #add_user(conn, tmp, "rando")

#print("Done. Adding Preferences...")
#for i in range(0, 100):
    #for j in range(0, 25):
        #tmp = "user" + str(j)
        #set_preference(conn, bool(random.randint(0,1)), bool(random.randint(0, 1)), get_user_id(conn, tmp), list_movies[random.randint(0, 1000)][9], rating=random.randint(1, 10))

#print("Done. Fetching rows randomly...")
#conn[1].execute("SELECT * FROM media ORDER BY RANDOM();")
#temp = conn[1].fetchall()

#print("Done. Clearing data...")
#clear_data(conn, "media")

#print("Done. Randomizing...")
#for item in temp:
    #conn[1].execute("INSERT INTO media VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s);", (item[0], item[1], item[2], item[3], item[4], item[5], item[6], item[7], item[8], item[9]))
print("Done...")

print(num_items(conn))
print(get_all_mediaTypes(conn))



for i in range(18400,100000000):
    x=Anime(1).title
    time.sleep(float(decimal.Decimal(random.randrange(99, 333))/100))
    try:
        print(i)
        a = Anime(i, timeout=30)
        print(type(a))
        if 'Ecchi' in a.genres or 'Hentai' in a.genres:
            print("nope: ", a.title)
            print(1/0)
        set_data(conn, a.title, a.type, int(a.aired.split()[2]), a.image_url, separator.join(a.genres), a.score, a.episodes*int(a.duration.split()[0]), str(-a.mal_id), summary=a.synopsis, certificate=a.rating)
        print(a.title)
    except:
        None
    
    time.sleep(float(decimal.Decimal(random.randrange(99, 333))/100))

    try:
        m = Manga(i, timeout=30)
        print(type(m))
        if 'Ecchi' in m.genres or 'Hentai' in m.genres:
            print("nope: ", m.title)
            print(1/0)
        set_data(conn, m.title, m.type, int(m.published.split()[2]), m.image_url, separator.join(m.genres), m.score, int(m.chapters), str(m.mal_id), summary=m.synopsis)
        print(m.title)
    except:
        None

    time.sleep(float(decimal.Decimal(random.randrange(99, 333))/100))

"""for i in range(1,1000000000):
    #set_data(pair, name, mediaType, year, link, genres, rating, running_time, ID, summary="None", certificate="PG"):
    try:
        #print(Anime(i).episodes*int(Anime(i).duration.split()[0]))
        print("Top: ", i)
        print(Anime(i).title)
        set_data(conn, Anime(i).title, Anime(i).type, int(Anime(i).aired.split()[2]), Anime(i).image_url, separator.join(Anime(i).genres), Anime(i).score, Anime(i).episodes*int(Anime(i).duration.split()[0]), str(-Anime(i).mal_id), summary=Anime(i).synopsis, certificate=Anime(i).rating)
        print(Anime(i).title)
        print(Manga(i).title)
        set_data(conn, Manga(i).title, Manga(i).type, int(Manga(i).published.split()[2]), Manga(i).image_url, separator.join(Manga(i).genres), Manga(i).score, int(Manga(i).chapters), str(Manga(i).mal_id), summary=Manga(i).synopsis)
        print(Manga(i).title)
    except:
        try:
            print("Bottom: ", i)
            print(Manga(i).title)
            set_data(conn, Manga(i).title, Manga(i).type, int(Manga(i).published.split()[2]), Manga(i).image_url, separator.join(Manga(i).genres), Manga(i).score, int(Manga(i).chapters), str(Manga(i).mal_id), summary=Manga(i).synopsis)
            print(Manga(i).title)
            print(Anime(i).title)
            set_data(conn, Anime(i).title, Anime(i).type, int(Anime(i).aired.split()[2]), Anime(i).image_url, separator.join(Anime(i).genres), Anime(i).score, Anime(i).episodes*int(Anime(i).duration.split()[0]), str(-Anime(i).mal_id), summary=Anime(i).synopsis, certificate=Anime(i).rating)
            print(Anime(i).title)
        except:
            None

"""

"""
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
print(get_user_recommendations(conn, str(get_user_id(conn, "username1"))))
print(get_user_recommendations(conn, str(get_user_id(conn, "username3"))))
print(get_user_recommendations(conn, str(get_user_id(conn, "username5"))))

clear_data(conn, "preferences")
clear_data(conn, "users")
"""
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

close_DBConnection(conn)
