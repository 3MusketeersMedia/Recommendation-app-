import http.client
import json

# can set up to return data that can be used by other function
def search(name):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "4e316e53d3mshc6d4451580c6d3fp1f652cjsnad69d8580ff7",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    # build the the link into right format url
    name = name.replace(" ", "%20")
    prefix = "/title/find?q="
    link = prefix + name

    # request the data
    conn.request("GET", link, headers=headers)
    res = conn.getresponse()
    data = res.read()

    # get data as json
    parsed = json.loads(data)
    # print(json.dumps(parsed, indent=4))

    # extract data
    # title_id is given in /title/tt3890160/, and tt3890160 is the id 
    title_id = parsed["results"][0]["id"]
    id = title_id.split("/") # grab just the id 

    # print(data.decode("utf-8"))

    return id[2]


# should return metadata of id (movies, shows, etc.) in JSON format
# "id":{
#   "title":{...}
#   "ratings":{...}
#   "metacritics":{...}
#   "releaseDate":{...}
#   "popularity":{...}
#   waysToWatch:{...}
#   "genre":{...}
#   "certificate": ...
# }

def get_metadata(id, region):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': "4e316e53d3mshc6d4451580c6d3fp1f652cjsnad69d8580ff7",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }
    
    # format in to a link
    prefix = "/title/get-meta-data?ids="
    region_format = "&region="
    link = prefix + id + region_format + region

    # request data 
    conn.request("GET", link, headers=headers)
    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))

    # get data as json
    parsed = json.loads(data)
    # print(json.dumps(parsed, indent=4))

    return parsed

# return list of images link of a given id (movies, shows, etc.)
# default limit is 3000. up to the value of totalImageCount
def get_image_urls(id, limit):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': "4e316e53d3mshc6d4451580c6d3fp1f652cjsnad69d8580ff7",
        'x-rapidapi-host': "imdb8.p.rapidapi.com"
    }

    # format in to a link
    prefix = "/title/get-all-images?tconst="
    limit_format = "&limit="
    link = prefix + id + limit_format +limit

    # request data
    conn.request("GET", link, headers=headers)
    res = conn.getresponse()
    data = res.read()

    # format into json to access data
    parsed = json.loads(data)

    # holds url of images
    images = []
    for i in range(len(parsed["resource"]["images"])):
        images.append(parsed["resource"]["images"][i]["url"])
    return images


id = search("baby driver")
metadata = get_metadata(id, "US")
urls_images = get_image_urls(id, "10")
