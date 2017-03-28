from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver
from bs4 import BeautifulSoup
import platform as pl
import re

def init_driver():

    platform = pl.system()
    if platform == 'Windows':
        driver = webdriver.Chrome(executable_path="../selenium_drivers/chromedriver_win32.exe")
    if platform == 'Linux':
        driver = webdriver.Chrome(executable_path="../selenium_drivers/chromedriver_64")
    wait = WebDriverWait(driver, 10)
    return driver, wait


def crawl_page(driver, wait):

    # wait
    wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'next 200')))

    # crawl movies
    html = driver.find_element_by_class_name('article').get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")
    movies = soup.find('div', id="mw-pages").find('div', class_="mw-content-ltr").find_all("a")
    for movie in movies:
        crawl_movie(movie)

    # redirect to next page, if exists
    try:
        next_page = driver.find_element_by_link_text('next 200')
        # print(next_page.get_attribute('href'))
        next_page.click()
        crawl_page(driver, wait)
    except:
        driver.close()

def crawl_movie(url):

    driver, wait = init_driver()
    driver.get("http://asianwiki.com" + url)
    html = driver.find_element_by_class_name('article').get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")

    rating = soup.find('span', id="w4g_rb_area-1").find('b').text
    votes_text = soup.find('span', id="w4g_rb_area-1").text
    votes = re.search("\([0-9]+", votes_text).group().replace("(","")

    print(rating, votes)
    driver.close()

HOME_PAGE = "http://asianwiki.com/index.php?title=Category:Comedy_films"

driver, wait = init_driver()
# driver.get(HOME_PAGE)
# crawl_page(driver, wait)

crawl_movie("/%2797_Aces_Go_Places")

# http://asianwiki.com/%2797_Aces_Go_Places