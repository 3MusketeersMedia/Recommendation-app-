# utility functions for users to use
from imdb import IMDb, IMDbError
from database import*
from apiRequests import *
from process_dataset import *
import random
import csv
import json
import pandas as pd
from imageScraper import *

# 6c0e5c9bfc8061e02d8fb8edb60aa8a9
# To install library: pip install tmdb3
import tmdbsimple as tmdb
tmdb.API_KEY = '6c0e5c9bfc8061e02d8fb8edb60aa8a9'

def get_imgurl_tmdbsimple(title, year):
    search = tmdb.Search()
    response = search.movie(query=title)
    # poster prefix: https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'poster_path'
    # for s in search.results:
    #     if 'release_date' in s:
    #         # print(s['release_date'], title)
    #         if year != None and s['release_date'][:4] == year:
    #             if s['poster_path'] != None:
    #                 return 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + s['poster_path']
    # print(len(search.results[0]))
    try:
        if(len(search.results[0]) != 0):
            if 'release_date' in search.results[0]:
                # print(s['release_date'], title)
                if year != None and year != '\'N' and search.results[0]['release_date'][:4] == year:
                    if search.results[0]['poster_path'] != None:
                        return 'https://www.themoviedb.org/t/p/w600_and_h900_bestv2/' + search.results[0]['poster_path']
    except IndexError:
        return None
    return None
# get_imgurl_tmdbsimple('Harry Potter and the Deathly Hallows: Part 1', '2010')
"""
This one uses RAPID API IMDb. Basic recommendation 
"""
# give you a list of similar movies
def search_for_similar():
    show_name = input("Name of show: ")
    show_id = search(show_name)
    recommended_ids = get_moreLikeThis(show_id, "US", "US")
    titles = []
    for i in recommended_ids:
        # get metadata of the given id
        title = get_metadata(i, "US")
        # get the title and put it into a list with pair id
        name = title[i]["title"]["title"]
        titles.append((name,i))
    return titles

def detailed_info(title, id):
    data = get_metadata(id, "US")
    print("Title: ", title)
    # print(id)
    print("Type: ", data[id]["title"]["titleType"])
    print("Running time (minutes): ", data[id]["title"]["runningTimeInMinutes"])
    print("Year: ", data[id]["title"]["year"])
    print("Rated: ", data[id]["certificate"])
    print("Rating: ", data[id]["ratings"]["rating"])
    print("Genres: ", end='')
    s = ""
    summary = " "
    for i in data[id]["genres"]:
        s+= i + " "
        # print(i, end=' ')
    print("\nImage URL: ", data[id]["title"]["image"]["url"])
    result = [title, data[id]["title"]["year"], s, data[id]["title"]["image"]["url"], data[id]["certificate"], data[id]["title"]["runningTimeInMinutes"], summary, data[id]["title"]["titleType"], id] 
    return result

"""
These uses IMDbPy library
"""
# get title, movie ids base on title
def get_movie_id(title):
    ids = []
    ia = IMDb()
    movies = ia.search_movie(title)
    for m in movies:
        id = m.getID()
        ids.append((m, id))
    return ids

# warning: some id do not have a rating so it will have to be skipped with try except:
def get_movie_rating(id):
    ia = IMDb()
    movie = ia.get_movie(id)
    return movie['rating']

# lst = get_movie_id('Matrix')
# for i, j in lst:
#     try:
#         rating = get_movie_rating(j)
#         print(i, rating)
#     except:
#         pass

def get_movie_info(id):
    ia = IMDb()
    m = ia.get_movie(id)
    print(m.keys())
    # use print(m.keys()) to see more options avaiable.
    # print(m['title'])
    # print(m['year'])
    # print(m['rating'])
    # directors = m['directors']
    # direcStr = ' '.join(map(str, directors))
    # print(f'directors: {direcStr}')
    # for genre in m['genres']:
    #     print(genre)

# get_movie_info(1234)
# return movie ids searched by keyword
def filter_by_keyword(keyword):
    ia = IMDb()
    movies = ia.get_keyword(keyword)
    ids = []
    for m in movies:
        ids.append(m.getID())
    return ids

def filter_by_genre(genre):
    movies = []
    data = imdb_basic()
    for row in data :
        genres_row = row[8]
        type_row = row[1]
        isAdult_row = row[4]
        title_row = row[3]
        if (genre in genres_row and isAdult_row == '0') and (type_row != 'short' or type_row !='tvEpisode'  or type_row != 'video'):
            if('Episode' not in title_row):
                movies.append(title_row)
    return movies

# movies = filter_by_genre('Comedy')
# for m in movies:
#     print(m)

def populate_database():
    exec(open("backend/database.py").read())
    connection = open_DBConnection()
    movies = []
    data = imdb_basic()
    # id, type, primary title, original title, isAdult, start, end, runtime, genre
    for row in data :
        if row[4] == 1:
            continue
        name = row[2]
        mediaType = row[1]
        year = row[5]
        link = get_imgurl_tmdbsimple(name, year)
        # link = getImage(row[0])  # movie image
        genres = row[8].replace(',', '|')
        rating = 0
        running_time = row[7]
        id = row[0][2:]
        if "N" in running_time:
            running_time = 0
        # print(id)
        set_data(connection, name, mediaType, year, link, genres, rating, running_time, id)
        # print(name, mediaType, year, link, genres, rating, running_time, id)
    #     movies.append((name, mediaType, year, link, genres, rating, running_time, id))
    # for m in movies:
    #     # print(m[3])
    #     set_data(connection, m[0], m[1], m[2], m[3], m[4], m[5], m[6], m[7])
    #     print("movie set:", m[0])
    close_DBConnection(connection)
    # return movies

# populate_database()

exec(open("backend/database.py").read())
connection = open_DBConnection()
print(num_items(connection, 'media'))
close_DBConnection(connection)

# get_movie_info(1234567)
# data base connection example

# exec(open("backend/database.py").read())
# connection = open_DBConnection()
# print(connection)
# # name, type, ID
# print(res[8])
# set_data(connection, res[0], "movie", res[8])
# list_of_items = get_by_id(connection, "tt4154756", table="media")
# for i in list_of_items:
#     print(i)
# delete_data(connection, "tt4154756", table="media")
# list_of_items = get_by_id(connection, "tt4154756", table="media")
# if list_of_items is not None:
#     for i in list_of_items:
#         print(i)
# else:
#     print("empty")
# close_DBConnection(connection)




# getting top 250 movies and bottom 100 movies
# https://www.youtube.com/watch?v=vzOdCPV7zvs

# moves goes from 1 to seven digit number 
# for i in range(1,99):
#     randNum = random.randint(1,99999)
#     ia = IMDb()
#     movie = ia.get_movie(randNum)
#     try:
#         if "Episode" in movie["title"]:
#             continue
#         print(i, movie["title"])
#     except::
#         print(e)
#         pass
# movie = ia.get_movie('9999999')
# print(movie["title"])
# top = ia.get_top250_movies()
# for movie in top:
#     id = movie.getID()
#     m = ia.get_movie(id)
#     print(id)
#     print(m.keys())
#     print(m['title'])
#     print(m['year'])
#     print(m['rating'])
#     directors = m['directors']
#     direcStr = ' '.join(map(str, directors))
#     print(f'directors: {direcStr}')
#     for genre in m['genres']:
#         print(genre)

# bottom = ia.get_bottom100_movies()

