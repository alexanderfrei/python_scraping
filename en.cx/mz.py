from bs4 import BeautifulSoup
import requests
import re

def parse_lineups(game_url):

    url = session.get(game_url)
    html = BeautifulSoup(url.text, "html.parser")
    lineups_href = html.find('a', {'id': 'lnkWinnerMembersEdit'})['href']

    url = session.get(EN + lineups_href)
    html = BeautifulSoup(url.text, "html.parser")
    tb = html.find('table', {'cellpadding': '3'})

    lineups = {}
    current_team = ''
    tr_ls = tb.find_all('tr')

    for tr in tr_ls:
        team_name = tr.find('span', class_='gold bold')
        if team_name:
            current_team = team_name.text
        a = tr.find('a', {'id': re.compile('WinnersRepeater_')})
        if a:
            lineups.setdefault(current_team, []).append(a.text)

    return lineups

### --------------------------------------------------------------------

EN = 'http://moscow.en.cx'
OUT = 'output/mz2'
INPUT = 'input/mz2'

### --------------------------------------------------------------------

with open(INPUT+".html", 'r', encoding='utf-8') as fl:
    html = fl.read()

soup = BeautifulSoup(html, "lxml")
tb = soup.find('table')

### team results

results = {}
tr_ls = tb.find('tbody').find_all('tr')
for tr in tr_ls[1:]:
    td_ls = tr.find_all('td')
    name = td_ls[1]
    for td in td_ls[2:]:
        results.setdefault(name.text, []).append(td.text)

with open(OUT+'_teams.csv', 'w', encoding='windows-1251') as out:
    for k in results:
        out.write(','.join([k]+results[k])+'\n')

### lineups

regex = re.compile('http:[^&]+')
session = requests.Session()

lineups = []

tb_head = tb.find('tbody').find('tr').find_all('td')
for td in tb_head:
    a = td.find('a')
    if a:
        game_url = regex.search(a['href'])[0].replace('%3D','=')
        lineups.append(parse_lineups(game_url))

with open(OUT+'_lineups.csv', 'w', encoding='windows-1251') as out:
    for i, dt in enumerate(lineups):
        for k in dt:
            out.write(','.join([str(i+1), k] + dt[k]) + '\n')
