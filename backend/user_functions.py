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
    print(title)
    print(id)
    print("Type: ", data[id]["title"]["titleType"])
    print("Running time (minutes): ", data[id]["title"]["runningTimeInMinutes"])
    print("Year: ", data[id]["title"]["year"])
    print("Genres: ", end='')
    # for i in data[id]["genres"]:
    #     print(i, end='')
    print("\n")

movie_list = search_for_similar()
for title, id in movie_list:
    detailed_info(title, id)