from bs4 import BeautifulSoup
import requests
import database


def extractName(item):
    header = item.find(class_='lister-item-header')
    return header.find('a').text


def extractID(item):
    link = item.find('a')['href']
    for segment in link.split('/'):
        if segment.startswith('tt'):
            return segment[2:]


def extractYear(item):
    header = item.find(class_='lister-item-header')
    text = header.find(class_='text-muted').text
    return int(text.split()[-1][1:-1])


def extractGenres(item):
    return item.find(class_='genre').text.strip()


def extractRating(item):
    return float(item.find(class_='ratings-imdb-rating').text)


def extractRunningTime(item):
    text = item.find(class_='runtime').text
    return int(text.split()[0])


def extractSummary(item):
    return item.findAll(class_='text-muted')[2].text.strip()


def extractCertificate(item):
    return item.find(class_='certificate').text

def loadTopBottom1000():
    topOrBottom = 'top'
    for _ in range(2):
        url = f'https://www.imdb.com/search/title/?groups={topOrBottom}_1000&count=250'
        loadMovies(url)
        topOrBottom = 'bottom'

def loadMovies(url):
    pair = database.open_DBConnection()
    for i in range(4):
        start = 250 * i + 1
        page = requests.get(f'{url}&start={start}')
        soup = BeautifulSoup(page.content, 'html.parser')
        for item in soup.findAll(class_='lister-item'):
            try:
                mediaItem = {
                    'name': extractName(item),
                    'mediaType': 'movie',
                    'year': extractYear(item),
                    'genres': extractGenres(item),
                    'rating': extractRating(item),
                    'running_time': extractRunningTime(item),
                    'summary': extractSummary(item),
                    'certificate': extractCertificate(item),
                    'id': extractID(item)
                }
                keys = list(mediaItem.keys())
                values = list(mediaItem.values())
                attributes = ','.join(keys)
                markers = ','.join(['%s' for _ in keys])
                sql = f'INSERT INTO MEDIA ({attributes}) VALUES ({markers})'
                pair[1].execute(sql, values)
            except Exception as e:
                print(e)


def loadImages():
    pair = database.open_DBConnection(True)
    pair[1].execute("SELECT id FROM media WHERE mediaType = 'movie' AND link IS NULL")
    for row in pair[1].fetchall():
        id = row['id']
        print(f'get image {id}')
        url = f'https://www.imdb.com/title/tt{id}/'
        try:
            page = requests.get(url)
            soup = BeautifulSoup(page.content, 'html.parser')
            posterDiv = soup.find(class_='poster')
            link = posterDiv.find('img')['src']
            pair[1].execute('UPDATE media SET link = %s WHERE id = %s', [link, id])
        except Exception as e:
            print(e)
