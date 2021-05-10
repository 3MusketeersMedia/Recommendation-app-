from bs4 import BeautifulSoup
import requests
import database


def loadRatings():
    pair = database.open_DBConnection()
    pair[1].execute('SELECT id FROM media WHERE rating = 0')
    result = pair[1].fetchall()
    for row in result:
        id = row[0]
        print(f'getting rating for {id}')
        try:
            page = requests.get(f'https://imdb.com/title/tt{id}')
            soup = BeautifulSoup(page.content, 'html.parser')
            rating = soup.find('div', class_='ratingValue').text
            sql = 'UPDATE MEDIA SET rating = %s WHERE id = %s'
            pair[1].execute(sql, [rating, id])
        except Exception as e:
            print(e)
