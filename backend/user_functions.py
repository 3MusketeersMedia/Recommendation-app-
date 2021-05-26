# utility functions for users to use
from logging import error
from process_dataset import tracks
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
import imdb_cred
import spotipy_cred

# To install library: pip install tmdb3
import tmdbsimple as tmdb
tmdb.API_KEY = imdb_cred.login['key']

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
    # print("Type: ", data[id]["title"]["titleType"])
    # print("Running time (minutes): ", data[id]["title"]["runningTimeInMinutes"])
    # print("Year: ", data[id]["title"]["year"])
    # print("Rated: ", data[id]["certificate"])
    # print("Rating: ", data[id]["ratings"]["rating"])
    # print("Genres: ", end='')
    s = ""
    summary = " "
    for i in data[id]["genres"]:
        s+= i + " "
    # print("\nImage URL: ", data[id]["title"]["image"]["url"])
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

def get_movie_plot(id):
    ia = IMDb()
    m = ia.get_movie(id)
    try:
        if m.get('plot') is not None:
            return m.get('plot')
    except error:
        return None
    return None

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

# populate database with movies
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
        summary = get_movie_plot(id)
        if link is None:
            link = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/No_image_3x4.svg/1200px-No_image_3x4.svg.png'
        if "N" in running_time:
            running_time = 0
        if "N" in year:
            year = 0
        set_data(connection, name, mediaType, year, link, genres, rating, running_time, id, summary)
    close_DBConnection(connection)

# populate database with music
def populate_tracks():
    exec(open("backend/database.py").read()) 
    sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=spotipy_cred.login['c_id'],
                                                           client_secret=spotipy_cred.login['c_secret']))
    connection = open_DBConnection()
    songs = []
    data = tracks()
    # id, name, artists, duration,  release date
    for row in data :
        id = row[0]
        results = sp.track(id)
        try:
            image = results['album']['images'][0]['url']
        except IndexError:
            image = None
        popularity = results['popularity']
        name = row[1]
        id = 'm' + id
        mediaType = 'Music'
        year = row[4][0:4]
        link = image
        genres = None
        rating = popularity / 10
        if image is None:
            image = 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/No_image_3x4.svg/1200px-No_image_3x4.svg.png'
        running_time = str((int(row[3])/1000) % 60)
        # print(id)
        set_data(connection, name, mediaType, year, link, genres, rating, running_time, id)
    close_DBConnection(connection)

# populate_tracks()
# populate_user()
populate_database()
