from bs4 import BeautifulSoup
import requests

def getImage(id):
    # print(id)
    url = f'https://www.imdb.com/title/{id}/'
    page = requests.get(url)

    soup = BeautifulSoup(page.content, 'html.parser')
    posterDiv = soup.find(class_='poster')
    posterImg = posterDiv.find('img')
    return posterImg['src']

# gets image for avengers: endgame
# print(getImage('tt4154796'))
