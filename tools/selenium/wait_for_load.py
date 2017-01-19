from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium import webdriver

driver = webdriver.Chrome()
driver.get("http://pythonscraping.com/pages/javascript/ajaxDemo.html")

try:
    element = WebDriverWait(driver, 10).until(ec.presence_of_element_located((By.ID, "loadedButton")))
finally:
    print(driver.find_element_by_id("content").text)
    driver.close()
