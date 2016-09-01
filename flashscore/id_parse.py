from selenium import webdriver
from selenium.common.exceptions import WebDriverException, NoSuchElementException
import time

"""
game:
    0. League
    1. Round
    2. Home
    3. Home goals
    4. Away
    5. Away goals
    6. Date
    7. Result
    8. Home goals 1st half
    9. Away goals 1st half
    10. Home goals 2nd half
    11. Away goals 2nd half
    12. Country
    13. Time of goals

stat (home/away):
    0/1. Ball Possession
    2/3. Goal Attempts
    4/5. Shots on Goal
    6/7. Corner Kicks
    8/9. Fouls
    10/11. Yellow Cards
    12/13. Red Cards

coefficients:
...
"""

htft_dict = {
    "1/1": 27,
    "1/d": 30,
    "1/2": 33,
    "d/1": 28,
    "d/d": 31,
    "d/2": 34,
    "2/1": 29,
    "2/d": 32,
    "2/2": 35,
    "": 0
}

score_dict = {
    "0:0": 1,
    "1:0": 2,
    "1:1": 3,
    "0:1": 4,
    "2:0": 5,
    "2:2": 7,
    "2:1": 6,
    "1:2": 8,
    "0:2": 9,
    "3:0": 10,
    "3:1": 11,
    "3:2": 12,
    "0:3": 16,
    "1:3": 15,
    "2:3": 14,
    "3:3": 13,
    "4:0": 18,
    "4:1": 19,
    "4:2": 20,
    "4:3": 21,
    "4:4": 17,
    "0:4": 25,
    "1:4": 24,
    "2:4": 23,
    "3:4": 22,
    "": 0
}

def click_xpath(wait,driver,xpath,sleep,message):
    try:
        wait.until(lambda d: d.find_element_by_xpath(xpath).is_displayed())
        time.sleep(sleep) # additional waiting for reliability, depends of internet connection quality
        driver.find_element_by_xpath(xpath).click()
        return True
    except WebDriverException:
        if message: print(message)
        return False

def search_wrapper(fun, xpath):
    try:
        return fun(xpath)
    except (WebDriverException, NoSuchElementException):
        return ""

def get_bk (arr,step):
    l = 1
    bk = [0]*5
    for line in arr:
        line = line.strip()
        if line == "William Hill": bk[0] = (l + step) / (step + 1)
        if line == "bet365": bk[1] = (l + step) / (step + 1)
        if line == "bwin": bk[2] = (l + step) / (step + 1)
        if line == "Paddy Power": bk[3] = (l + step) / (step + 1)
        if line == "Unibet": bk[4] = (l + step) / (step + 1)
        l+=1
    return bk

"""
alt: number of issues
td: 1st coefficient's column
cols: total number of columns in markup
"""

def get_tab(xpath,cols,alt,td,shift,coef_par,driver):
    coef = driver.find_element_by_xpath("//*[@id='odds_{0}']/tbody".format(xpath)).text.split('\n')
    start = [["" for y in range(3)] for x in range(5)]
    bk = get_bk(coef,cols)
    for i in range(0,5):
        for y in range(0,alt):
            if bk[i]:
                start[i][y] = driver.find_element_by_xpath("//*[@id='odds_{0}']/tbody/tr[{1}]/td[{2}]/span".
                                                           format(xpath,str(bk[i]),str(y+td))).get_attribute("eu")
    for i in range(0, 5):
        for y in range(0, alt):
            coef_par[shift+i*alt+y] = start[i][y]

class IdParser:
    def __init__(self):
        self.htft = ""

    def get_game(self,game_id):
        game_par = ['']*14
        driver = webdriver.Chrome()
        driver.get("http://www.flashscore.com/match/{0}/#match-summary/".format(game_id))
        tournament=search_wrapper(driver.find_element_by_xpath,'//*[@id="detcon"]/table/thead/tr/th/div').text.split('-')
        tournament = [t.strip() for t in tournament]
        game_par[0] = tournament[0]
        game_par[1] = " ".join(tournament[1:])
        game_par[12] = tournament[0].split(':')[0]

        game_par[2]=search_wrapper(driver.find_element_by_xpath,"//*[@id='flashscore_column']/table/tbody/tr[1]/td[1]/span/a").text
        game_par[3]=search_wrapper(driver.find_element_by_xpath,"//*[@id='flashscore_column']/table/tbody/tr[1]/td[2]/span[1]").text
        game_par[4]=search_wrapper(driver.find_element_by_xpath,"//*[@id='flashscore_column']/table/tbody/tr[1]/td[3]/span/a").text
        game_par[5]=search_wrapper(driver.find_element_by_xpath,"//*[@id='flashscore_column']/table/tbody/tr[1]/td[2]/span[3]").text
        game_par[6]=search_wrapper(driver.find_element_by_xpath,"//*[@id='utime']").text[0:10]
        game_par[7]=search_wrapper(driver.find_element_by_xpath,"//*[@id='flashscore_column']/table/tbody/tr[3]/td").text
        game_par[8]=search_wrapper(driver.find_element_by_class_name,"p1_home").text
        game_par[9]=search_wrapper(driver.find_element_by_class_name,"p1_away").text
        game_par[10]=search_wrapper(driver.find_element_by_class_name,"p2_home").text
        game_par[11]=search_wrapper(driver.find_element_by_class_name,"p2_away").text

        try:
            goals=driver.find_elements_by_css_selector("*[class^='icon-box soccer-ball']")
            goals=[p.find_element_by_xpath('../div[1]').text.replace("'","").replace(" ","") for p in goals]
            last = 0
            for i,g in enumerate(goals):
              g = int(g[:2])
              if g > last: last = g
              if g < last: goals[i] = None
            while None in goals: goals.remove(None)
        except (WebDriverException, NoSuchElementException):
            pass
        game_par[13]=",".join(goals)

        if game_par[8] and game_par[9] and game_par[3] and game_par[5]:
            if int(game_par[8]) > int(game_par[9]): self.htft = "1/";
            if int(game_par[8]) == int(game_par[9]): self.htft = "d/";
            if int(game_par[8]) < int(game_par[9]): self.htft = "2/";
            if int(game_par[3]) > int(game_par[5]): self.htft += "1";
            if int(game_par[3]) == int(game_par[5]): self.htft += "d";
            if int(game_par[3]) < int(game_par[5]): self.htft += "2";

        driver.close()
        return game_par

    def get_stat(self, game_id):
        driver = webdriver.Chrome()
        stat_par = ['']*14
        try:
            driver.get("http://www.flashscore.com/match/{0}/#match-statistics;0".format(game_id))
            stat = driver.find_element_by_xpath("// *[@id = 'tab-statistics-0-statistic']/table/tbody").text.split('\n')
        except (WebDriverException, NoSuchElementException):
            driver.close()
            return stat_par
        for i,s in enumerate(stat):
            if s == "Ball Possession":
                stat_par[0] = stat[i-1]
                stat_par[1] = stat[i+1]
            if s == "Goal Attempts":
                stat_par[2] = stat[i-1]
                stat_par[3] = stat[i+1]
            if s == "Shots on Goal":
                stat_par[4] = stat[i-1]
                stat_par[5] = stat[i+1]
            if s == "Corner Kicks":
                stat_par[6] = stat[i-1]
                stat_par[7] = stat[i+1]
            if s == "Fouls":
                stat_par[8] = stat[i-1]
                stat_par[9] = stat[i+1]
            if s == "Yellow Cards":
                stat_par[10] = stat[i-1]
                stat_par[11] = stat[i+1]
            if s == "Red Cards":
                stat_par[12] = stat[i-1]
                stat_par[13] = stat[i+1]

        driver.close()
        return stat_par

    def get_coef(self, game_id):

        sleep = 1.5 # waiting in manual mode
        coef_par = ['']*55
        driver = webdriver.Chrome()

        # 1x2
        try:
            driver.get("http://www.flashscore.com/match/{0}#odds-comparison;1x2-odds;full-time"
                      .format(game_id))
            time.sleep(sleep)
            get_tab("1x2",4,3,2,0,coef_par,driver)
        except NoSuchElementException:
            driver.close()
            return coef_par

        # Draw no bet
        try:
            driver.find_element_by_xpath("//*[@id='bookmark-moneyline']/span/a").click()
            time.sleep(sleep)
            get_tab("dnb",3,2,2,15,coef_par,driver)
        except NoSuchElementException:
            pass

        # Over/Under
        try:
            driver.find_element_by_xpath("//*[@id='bookmark-under-over']/span/a").click()
            time.sleep(sleep)
            get_tab("ou_2.5",4,2,3,25,coef_par,driver)
        except NoSuchElementException:
            pass

        # Score
        try:
            driver.find_element_by_xpath("//*[@id='bookmark-correct-score']/span/a").click()
            time.sleep(sleep)
            score = driver.find_element_by_xpath("//*[@id='flashscore_column']/table/tbody/tr[1]/td[2]") \
                .text.replace('-', ':').strip(' \r\n')
            cs = score_dict[score]
            if cs: get_tab("correct_score_"+str(cs),3,1,3,35,coef_par,driver)
        except NoSuchElementException:
            pass

        # BTS
        try:
            driver.find_element_by_xpath("//*[@id='bookmark-both-teams-to-score']/span/a").click()
            time.sleep(sleep)
            get_tab("both_teams_to_score",3,2,2,40,coef_par,driver)
        except NoSuchElementException:
            pass

        # HTFT
        try:
            driver.find_element_by_xpath("//*[@id='bookmark-ht-ft']/span/a").click()
            time.sleep(sleep)
            hf = htft_dict[self.htft]
            if hf: get_tab("htft_"+str(hf),3,1,3,50,coef_par,driver)
        except NoSuchElementException:
            pass

        driver.close()
        return coef_par


