from selenium import webdriver
from bs4 import BeautifulSoup

def init_phantomjs_driver(*args, **kwargs):

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
        "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        'Connection': 'keep-alive'
    }

    for key, value in headers.items():
        webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.customHeaders.{}'.format(key)] = value

    webdriver.DesiredCapabilities.PHANTOMJS['phantomjs.page.settings.userAgent'] = headers['User-Agent']

    driver =  webdriver.PhantomJS(*args, **kwargs)
    driver.set_window_size(1200,900)

    return driver

service_args = [
    '--proxy=localhost:9050',
    '--proxy-type=socks5',
    '--ignore-ssl-errors=true'
]

driver = init_phantomjs_driver(service_args=service_args)

driver.get('http://icanhazip.com/')
print(driver.find_element_by_tag_name("html").text)

driver.get('https://www.whatismybrowser.com/detect/what-http-headers-is-my-browser-sending')
print(driver.find_element_by_tag_name("tbody").text)

driver.close()
