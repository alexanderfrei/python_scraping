import re
# import sys
# sys.setrecursionlimit(100000)

from bs4 import BeautifulSoup

with open("input/ic.html", 'r', encoding='utf-8') as fl:
    html = fl.read()

soup = BeautifulSoup(html, "lxml")
tb = soup.find('table')
tr_ls = tb.find('tbody').find_all('tr')

results = {}

for tr in tr_ls[1:]:
    name = tr.find('a')
    td_ls = tr.find_all('td')
    for td in td_ls[2:]:
        results.setdefault(name.text, []).append(td.text)

# print(results)
with open('output/IC.csv', 'w', encoding='windows-1251') as out:
    for k in results:
        out.write(','.join([k]+results[k])+'\n')