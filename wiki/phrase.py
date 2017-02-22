import socks
import socket
import requests
from bs4 import BeautifulSoup
import re

####################################################
# configuring requests session

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Connection': 'keep-alive'
}

session = requests.Session()
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
session.headers = headers
socket.socket = socks.socksocket

####################################################

url = "https://ru.wiktionary.org/wiki/%D0%9F%D1%80%D0%B8%D0%BB%D0%BE%D0%B6%D0%B5%D0%BD%D0%B8%D0%B5:%D0%A1%D0%BF%D0%B8%D1%81%D0%BE%D0%BA_%D1%84%D1%80%D0%B0%D0%B7%D0%B5%D0%BE%D0%BB%D0%BE%D0%B3%D0%B8%D0%B7%D0%BC%D0%BE%D0%B2_%D1%80%D1%83%D1%81%D1%81%D0%BA%D0%BE%D0%B3%D0%BE_%D1%8F%D0%B7%D1%8B%D0%BA%D0%B0"
url = session.get(url)
bsObj = BeautifulSoup(url.text, "html.parser")
tables = bsObj.findAll("table", {"class": "wikitable sortable"})

with open('phrase.txt','w') as file:
    for table in tables:
        trs = table.find_all("tr")
        for tr in trs:
            if tr.find("a"):
                phrase = tr.find("a")
            else:
                phrase = tr.find("td")
            if phrase:
                file.write(phrase.text + "\n")

session.close()
