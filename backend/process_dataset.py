import csv
import json
import pandas as pd
from datetime import datetime
def data_json(filename):
    data = {}
    data['movies'] = []
    # open cvs file
    with open(filename,'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) #skip first row i.e header of csv file
        # https://data.world/himan/imdb-movie-dataset/workspace/file?filename=movie_data.csv
        for row in reader:
            # create a json format
            data['movies'].append(
                {
                    'title' : row[5],
                    'director' : row[0],
                    'duration' : row[1],
                    'genres' : row[3],
                    'rating' : row[13],
                    'year' : row[12],
                    'country' : row[11],
                    'language' : row[10]
                }
            )
    with open('json_data.json', 'w') as outfile:
        json.dump(data, outfile)

# dataset until 2016
# filename = 'backend/Movie_Data.csv'
# data_json(filename)

# with open('json_data.json') as json_file:
#     data = json.load(json_file)
#     print(json.dumps(data, ensure_ascii=False,indent=4, sort_keys=True))


# processing imdb_data_basic
# filename = 'backend/Movie_Data.csv'
def imdb_basic():
    data = []
    # data['movies'] = []
    # open cvs file
    with open('backend/imdb_data_basic.csv','r', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader) #skip first row i.e header of csv file
        for row in reader:
            link = "https://www.imdb.com/title/" + row[0]
            currentYear = datetime.today().year
            # id, type, primary title, original title, isAdult, start, end, runtime, genre, imdb link
            # print(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], link)
            if row[5] >= '2020' and row[5] <= str(currentYear) and row[1] == 'movie':
                data.append((row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], link))
    return data
            # create a json format
    #         data['movies'].append(
    #             {
    #                 'title' : row[5],
    #                 'director' : row[0],
    #                 'duration' : row[1],
    #                 'genres' : row[3],
    #                 'rating' : row[13],
    #                 'year' : row[12],
    #                 'country' : row[11],
    #                 'language' : row[10]
    #             }
    #         )
    # with open('json_data.json', 'w') as outfile:
    #     json.dump(data, outfile)

# tsv_file='imdb_data_basic.tsv'
# csv_table=pd.read_table(tsv_file,sep='\t')
# csv_table.to_csv('imdb_data_basic.csv',index=False)


# filename = 'imdb_data_basic.csv'
# imdb_basic(filename)
