execfile("database.py")
two = open_DBConnection()

set_data(two, "vinu show", "tv show", 1)
set_data(two, "vinu show", "movie", 2)
set_data(two, "vinu show", "short film", 3)
set_data(two, "belen show", "movie", 4)
set_data(two, "booby show", "movie", 5)
set_data(two, "dooby show", "anime", 6)

stuff = get_by_name(two, "vinu show")
print(stuff)

stuff = get_by_id(two, 6)
print(stuff)

stuff = get_by_mediaType(two, "movie")
print(stuff)

clear_data(two)
close_DBConnection(two)
