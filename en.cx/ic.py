import re
from bs4 import BeautifulSoup

with open("ic.html", 'r', encoding='utf-8') as fl:
    html = fl.read()

soup = BeautifulSoup(html, "lxml")
tb = soup.find('table')
tr_ = tb.find_all('tr')

names = []

for tr in tr_:
    name = tr.find('a')
    if name:
        if name.text.find('игра') == -1:
            td_ = tr.find_all('td')
            print(name.text)
