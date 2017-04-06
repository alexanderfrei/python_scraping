import re
import requests
from bs4 import BeautifulSoup

login_url = 'http://demo.en.cx/Login.aspx'
game_url = "http://demo.en.cx/gameengines/encounter/play/26533"

credentials = {'Login': 'frei_demo',
               'Password': 'enkahuenka1',
               'persistent': '1'}

with requests.Session() as s:

    # login
    r = s.post(login_url, data=credentials)
    game_page = s.get(game_url)
    html = BeautifulSoup(game_page.text, "html.parser")

    ### вбитие
    level_id = html.find("input", {"name": "LevelId"}).attrs['value']
    level_number = html.find("input", {"name": "LevelNumber"}).attrs['value']

    code = "Я медленно вбиваю код"
    bonus_code = "..и закурил ///\&*%%$@##@!~"

    code_data = {"LevelId": level_id,
                 "LevelNumber": level_number,
                 "LevelAction.Answer": code}
    bonus_data = {"LevelId": level_id,
                  "LevelNumber": level_number,
                  "BonusAction.Answer": bonus_code}

    # s.post(game_url, data=bonus_data)

    ### парсим коды

    # right_html = html.findAll("span", {"class": "color_correct"})
    # bonus_html = html.findAll("span", {"class": "color_bonus"})
    # all_codes_html = html.findAll("span", {"class": re.compile("color_correct|color_bonus")})
    #
    # right_codes = list(set([code.text.strip() for code in right_html]))
    # bonus_codes = list(set([code.text.strip() for code in bonus_html]))
    # all_right_codes = right_codes + bonus_codes
    # all_right_codes_2 = list(set([code.text.strip() for code in all_codes_html]))

