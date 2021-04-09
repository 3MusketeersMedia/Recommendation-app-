import http.client
import json

key = "4e316e53d3mshc6d4451580c6d3fp1f652cjsnad69d8580ff7"
host = "imdb8.p.rapidapi.com"
# can set up to return data that can be used by other function
def search(name):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")
    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': host
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
        'x-rapidapi-key': key,
        'x-rapidapi-host': host
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
        'x-rapidapi-key': key,
        'x-rapidapi-host': host
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

# return a summary of the selected movie id. region can be defaulted to US
def get_overview(id, region):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': host
    }

    # format in to a link
    prefix = "/title/get-overview-details?tconst="
    region_format = "&currentCountry"
    link = prefix + id + region_format + region

    conn.request("GET", link, headers=headers)

    res = conn.getresponse()
    data = res.read()

    # print(data.decode("utf-8"))

    # get data as json
    parsed = json.loads(data)
    # print(json.dumps(parsed, indent=4))
    return parsed["plotSummary"]["text"]

# up to 14 recommendations by IMDb
# currentCountry and purchaseCountry are defaulted to US
def get_moreLikeThis(id, currentCountry, purchaseCounty):
    conn = http.client.HTTPSConnection("imdb8.p.rapidapi.com")

    headers = {
        'x-rapidapi-key': key,
        'x-rapidapi-host': host    
    }

    # format in to a link
    prefix = "/title/get-more-like-this?tconst="
    currentCountry_format = "&currentCountry="
    purchaseCountry_format = "&purchaseCountry="
    link = prefix + id + currentCountry_format + currentCountry + purchaseCountry_format + purchaseCounty

    conn.request("GET", link, headers=headers)

    res = conn.getresponse()
    data = res.read()

    # get data as json
    parsed = json.loads(data)
    # print(json.dumps(parsed, indent=4))

    # all 14 ids corresponding to movies, shows, etc. recommended by IMDb
    ids = []
    for i in parsed:
        # title_id is given in /title/tt3890160/, and tt3890160 is the id 
        number = i.split("/") # grab just the id 
        ids.append(number[2])
    return ids

id = search("baby driver")
metadata = get_metadata(id, "US")
urls_images = get_image_urls(id, "10")
summary = get_overview(id, "US")
recommended_ids = get_moreLikeThis(id, "US", "US")



