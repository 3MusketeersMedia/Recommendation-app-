import csv
import json
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
filename = 'backend/Movie_Data.csv'
data_json(filename)

with open('json_data.json') as json_file:
    data = json.load(json_file)
    print(json.dumps(data, ensure_ascii=False,indent=4, sort_keys=True))