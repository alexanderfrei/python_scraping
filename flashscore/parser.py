import re
import datetime as dt
import logging, sys
import codecs, os
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from id_parse import *

################################################################################################
################################################################################################

'''
Command line parameters:
1: url
2: dbname
3: start game ID (optional)
4: end game ID (optional)
'''

try:
    url = sys.argv[1]
    db = sys.argv[2]
except IndexError:
    sys.exit("Input url and db name!")
try:
    start_game = sys.argv[3]
    end_game = sys.argv[4]
except IndexError:
    pass

################################################################################################
################################################################################################

local = "D:\\Betting\db"

log = os.path.join(local,"log.txt")
logging.basicConfig(filename=log,level=logging.INFO)
start = dt.datetime.now()
logging.info('\nstart time: {0}\nurl: {1}\ndb: {2}'.format(str(start),url,db))

db_file = os.path.join(local,db,db+".txt")

driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)
driver.get("http://www.flashscore.com/soccer/{0}/results/".format(url))

################################################################################################
################################################################################################

# clicking the buttons `get more matches`

click_xpath(wait,driver,'//*[@id="cookie-law-content"]/div/span',2,'')

i = 0
while i < 10:
    if not click_xpath(wait,driver,'//*[@id="tournament-page-results-more"]/tbody/tr/td/a',2,'Processing games..'):
        break
    i+=1
    print("Clicking..")

# fill list of matches ID

id_list, tr, table_num = [], 1, 0
game_id, table = "", ""
while table_num < 10:
    while tr < 1000:
        try:
            game_id = driver.find_element_by_xpath("//*[@id='fs-results']/table{1}/tbody/tr[{0}]".
                                                    format(str(tr),table)).get_attribute("Id")
            match = re.fullmatch("^(g_1_)[\w]*",str(game_id))
            if match is not None and game_id[4:] not in id_list:
                id_list.append(game_id[4:])
        except NoSuchElementException:
            tr = 1
            break
        tr+=1
    table_num+=1; table = "[{0}]".format(str(table_num))

# write to file

print("Writing file..")
game_list, stat_list, coef_list = [], [], []
parse = True if not start_game in id_list else False
for n, game_id in enumerate(id_list):
    if game_id == start_game: parse = True
    if parse:
        print("Writing game: {0} #{1} ".format(game_id, n+1))
        parser = IdParser()
        game_list = parser.get_game(game_id)
        stat_list = parser.get_stat(game_id)
        coef_list = parser.get_coef(game_id)
        with codecs.open(db_file, 'a', encoding='utf-8') as wf:
            wf.write("{0},{1},{2},{3}\n"
                    .format(game_id,",".join(stat_list),",".join(coef_list),",".join(game_list)))
    if game_id == end_game: break

################################################################################################
################################################################################################

end = dt.datetime.now()
logging.info('\nend time:{1}\ngames processed:{0}\nlength, min:{2:.0f}\n'.
             format(str(len(id_list)),str(end),(end - start).seconds / 60))
driver.close()
