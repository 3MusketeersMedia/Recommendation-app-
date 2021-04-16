# utility functions for users to use
from apiRequests import *

done = False

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
    print("Genres: ", end='')
    s = ""
    summary = " "
    for i in data[id]["genres"]:
        s+= i + " "
        # print(i, end=' ')
    print("\nImage URL: ", data[id]["title"]["image"]["url"])
    result = [title, data[id]["title"]["year"], s, data[id]["title"]["image"]["url"], data[id]["certificate"], data[id]["title"]["runningTimeInMinutes"], summary, data[id]["title"]["titleType"], id] 
    return result

# loading test file
with open('test_file.json', 'r') as file:
    info = file.read().rstrip('\n')
parsed = json.loads(info)
res = detailed_info(parsed["tt4154756"]["title"]["title"], "tt4154756")
# for i in res:
#     print(i)

# movie_list = search_for_similar()
# for title, id in movie_list:
#     detailed_info(title, id)


exec(open("database/database.py").read())

connection = open_DBConnection()

# print(connection)
# name, type, ID
set_data(connection, res[0], "movie", res[8])
list_of_items = get_by_id(connection, "tt4154756", table="media")
for i in list_of_items:
    print(i)
delete_data(connection, "tt4154756", table="media")
list_of_items = get_by_id(connection, "tt4154756", table="media")
if list_of_items is not None:
    for i in list_of_items:
        print(i)
else:
    print("empty")
close_DBConnection(connection)