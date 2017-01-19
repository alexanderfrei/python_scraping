from urllib.request import urlopen
from bs4 import BeautifulSoup
import re

ITER = 3

pages = set()
def getLinks(pageUrl):
    global pages
    while len(pages) < ITER:

        html = urlopen("http://en.wikipedia.org"+pageUrl)
        bsObj = BeautifulSoup(html, "html.parser")
        try:
            print(bsObj.h1.get_text())
            print(bsObj.find(id ="mw-content-text").findAll("p")[0])
            print(bsObj.find(id="ca-edit").find("span").find("a").attrs['href'])
        except AttributeError:
            print("This page is missing something! No worries though!")

        for link in bsObj.findAll("a", href=re.compile("^(/wiki/)")):
            if 'href' in link.attrs:
                if link.attrs['href'] not in pages and len(pages) < ITER:
                    #We have encountered a new page
                    newPage = link.attrs['href']
                    print("----------------"+newPage)
                    pages.add(newPage)
                    getLinks(newPage)
getLinks("")

