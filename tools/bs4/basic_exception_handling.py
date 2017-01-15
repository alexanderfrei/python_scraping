from urllib.request import urlopen
from urllib.error import HTTPError
from bs4 import BeautifulSoup

def getTitle(url):
    try:
        html = urlopen(url) # urllib url open
    except HTTPError as e:
        print(e)
        return None
    try:
        bsObj = BeautifulSoup(html.read(), 'lxml') # html.read() return url text
        title = bsObj.body.h1
    except AttributeError as e:
        print(e)
        return None
    return title

title = getTitle("http://www.pythonscraping.com/exercises/exercise1.html")
print(title, type(title)) # bs4 type tag