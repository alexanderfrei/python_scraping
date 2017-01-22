from selenium import webdriver
from bs4 import BeautifulSoup
import re
import os
import socks
import socket
import requests
from io import BytesIO
from PIL import Image


DOWNLOAD_PATH = "/media/frei/data/Wallpapers/wallpaper_ru/"

####################################################
# configuring webdriver

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Connection': 'keep-alive'
}


def init_phantomjs_driver(*args, **kwargs):

    global headers
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

# driver = init_phantomjs_driver(service_args=service_args)
# webdriver ip test
# driver.get('http://ipinfo.io/ip')
# print(driver.find_element_by_tag_name("html").text)
# driver.close()

####################################################
# configuring requests session

session = requests.Session()
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
session.headers = headers
socket.socket = socks.socksocket
# session ip test
# ip_test = session.get('http://ipinfo.io/ip')
# print(session.headers, ip_test.text)

for page in range(1, 14):
    print("http://www.wallpapers.ru/index/page{}/ is loading..".format(page))
    req = session.get("http://www.wallpapers.ru/index/page{}/".format(page))
    bs = BeautifulSoup(req.text, "html.parser")
    a_tags = bs.findAll("a", {"class":"imgpreview"}, href=re.compile(".*(jpg|png|jpeg|bmp|gif|tiff)$"))
    for a_tag in a_tags:
        if a_tag is not None:
            url = a_tag.attrs["href"]
            if url is not None:
                print(url)
                base = os.path.basename(url)
                r = session.get(url)
                if not os.path.exists(DOWNLOAD_PATH + base):
                    image = Image.open(BytesIO(r.content))
                    try:
                        image.save(DOWNLOAD_PATH + base)
                    except OSError:
                        pass

session.close()
