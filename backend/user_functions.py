# utility functions for users to use
from imdb import IMDb, IMDbError
from database import*
from apiRequests import *
from process_dataset import *
from model import *
import random
import csv
import json
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from imageScraper import *
# 6c0e5c9bfc8061e02d8fb8edb60aa8a9
# To install library: pip install tmdb3
import tmdbsimple as tmdb
tmdb.API_KEY = '6c0e5c9bfc8061e02d8fb8edb60aa8a9'

def get_imgurl_tmdbsimple(title, year):
    search = tmdb.Search()
    response = search.movie(query=title)
    # poster prefix: https://www.themoviedb.org/t/p/w600_and_h900_bestv2/'poster_path'
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

def get_movie_info(id):
    ia = IMDb()
    m = ia.get_movie(id)
    # print(m.keys())
    print(m['title'])
    print(m.keys())

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
        genres = row[8].replace(',', '|')
        rating = 0
        running_time = row[7]
        id = row[0][2:]
        if "N" in running_time:
            running_time = 0
        if "N" in year:
            year = 0
        # print(id)
        set_data(connection, name, mediaType, year, link, genres, rating, running_time, id)
        # print(name, mediaType, year, link, genres, rating, running_time, id)
    close_DBConnection(connection)

# populate_database()
# populate_user()
# exec(open("backend/database.py").read())
# connection = open_DBConnection()
# print(get_all_users(connection))
# close_DBConnection(connection)
# user_recs = get_user_recommendations('username', 'password_hash')
# for id in user_recs:
#     get_movie_info(id)

sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id="12ba660d977341309ab9343a38e9456a",
                                                           client_secret="0c9d62373fb84dc2adae9c7c9855b1f5"))

results = sp.search(q='lil nax', limit=20)
for idx, track in enumerate(results['tracks']['items']):
    print(idx, track['name'])