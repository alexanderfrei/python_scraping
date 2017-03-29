import csv
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
        # driver = webdriver.Chrome(executable_path="../selenium_drivers/chromedriver_win32.exe")
        driver = webdriver.PhantomJS(executable_path="../selenium_drivers/phantomjs.exe")
    if platform == 'Linux':
        driver = webdriver.Chrome(executable_path="../selenium_drivers/chromedriver_64")
    wait = WebDriverWait(driver, 10)
    return driver, wait


def crawl_page(driver, wait, file):

    # wait
    wait.until(ec.element_to_be_clickable((By.LINK_TEXT, 'next 200')))
    print("--- Page loaded ---")

    # crawl movies
    html = driver.find_element_by_class_name('article').get_attribute('innerHTML')
    soup = BeautifulSoup(html, "html.parser")
    movies = soup.find('div', id="mw-pages").find('div', class_="mw-content-ltr").find_all("a")
    for movie in movies:
        crawl_movie(movie.attrs['href'], file)

    # redirect to next page, if exists
    try:
        next_page = driver.find_element_by_link_text('next 200')
        next_page.click()
        crawl_page(driver, wait, file)
    except:
        driver.close()


def crawl_movie(url, file):

    driver_m, wait = init_driver()
    driver_m.get("http://asianwiki.com" + url)
    if driver_m.find_element_by_class_name('article'):
        html = driver_m.find_element_by_class_name('article').get_attribute('innerHTML')
        soup = BeautifulSoup(html, "html.parser")

        movie = [""] * 9
        movie[8] = url

        if soup.find('span', id="w4g_rb_area-1"):
            votes_text = soup.find('span', id="w4g_rb_area-1").text
            if re.search("\([0-9]+", votes_text):
                movie[1] = re.search("\([0-9]+", votes_text).group().replace("(","")
            if soup.find('span', id="w4g_rb_area-1").find('b'):
                movie[0] = soup.find('span', id="w4g_rb_area-1").find('b').text

        description = soup.find_all('li')
        for value in description:
            s = value.text
            pattern=r'(.*Movie:)(.*)'
            if re.match(pattern, s):
                movie[2] = re.search(pattern, s).group(2).strip()
            pattern = r'(.*Writer:)(.*)'
            if re.match(pattern, s):
                movie[3] = re.search(pattern, s).group(2).strip()
            pattern = r'(.*Director:)(.*)'
            if re.match(pattern, s):
                movie[4] = re.search(pattern, s).group(2).strip()
            pattern = r'(.*Country:)(.*)'
            if re.match(pattern, s):
                movie[5] = re.search(pattern, s).group(2).strip()
            pattern = r'(.*Runtime:)(.*)(min)'
            if re.match(pattern, s):
                movie[6] = re.search(pattern, s).group(2).strip()
            pattern = r'(.*Release Date:)(.*,)(.*)'
            if re.match(pattern, s):
                movie[7] = re.search(pattern, s).group(3).strip()

        print(movie[2], movie[8])
        file.writerow(movie)

    driver_m.close()


HOME_PAGE = "http://asianwiki.com/index.php?title=Category:Comedy_films"
FILE_NAME = "comedy_part1.csv"

file = csv.writer(open(FILE_NAME, "w"),
                  delimiter=';',
                  quoting=csv.QUOTE_NONE,
                  escapechar='\\',
                  lineterminator='\n')

driver, wait = init_driver()
driver.get(HOME_PAGE)
crawl_page(driver, wait, file)
