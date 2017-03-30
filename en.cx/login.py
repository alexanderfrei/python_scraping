import time
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
        driver = webdriver.PhantomJS(executable_path="../selenium_drivers/phantomjs.exe")
    if platform == 'Linux':
        driver = webdriver.Chrome(executable_path="../selenium_drivers/chromedriver_64")
        # driver = webdriver.PhantomJS(executable_path="../selenium_drivers/phantomjs_64")
    wait = WebDriverWait(driver, 5)
    return driver, wait


HOME_PAGE = "http://moscow.en.cx/"
driver, wait = init_driver()
driver.get(HOME_PAGE)

log_id = "ctl14_ctl04_ctl00_lnkLogin"
wait.until(ec.element_to_be_clickable((By.ID, log_id)))

log_in = driver.find_element_by_id(log_id).click()

print("--- Page loaded ---")

username = driver.find_element_by_id("txtLogin")
password = driver.find_element_by_id("txtPassword")

username.send_keys("Борода") # <- логин
password.send_keys("Борода-пароль") # <- пароль

driver.find_element_by_class_name("glassubmit").click()


time.sleep(30)

driver.close()


