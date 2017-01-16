from urllib.request import urlopen
from bs4 import BeautifulSoup
import datetime
import random
import re

START = "/wiki/Kevin_Bacon"
ITER = 10

random.seed(datetime.datetime.now())
def getLinks(articleUrl):
    html = urlopen("http://en.wikipedia.org"+articleUrl)
    bsObj = BeautifulSoup(html, "html.parser")
    return bsObj.find("div", {"id":"bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$"))
links = getLinks(START)
i = 0
while i < ITER:
    newArticle = links[random.randint(0, len(links)-1)].attrs["href"]
    print(i + 1, newArticle, len(newArticle))
    i += 1
    links = getLinks(newArticle)

