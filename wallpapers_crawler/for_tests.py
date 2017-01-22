import os
import socks
import socket
import requests
from io import BytesIO
from PIL import Image

url = "http://www.wallpapers.ru/uploads/images/00/20/83/2016/12/04/wallpapers_ru_godgory_2560x1707_interspace.jpg"
base = os.path.basename(url)
DOWNLOAD_PATH = "/media/frei/data/Wallpapers/wallpaper_ru/"


headers = {"User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
           "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
           'Connection': 'keep-alive'
           }
session = requests.Session()
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
session.headers = headers
socket.socket = socks.socksocket

# session ip test
# ip_test = session.get('http://ipinfo.io/ip')
# print(session.headers, ip_test.text)

# r = session.get(url)
# image = Image.open(BytesIO(r.content))
# image.save (DOWNLOAD_PATH + base)

html = session.get("http://www.wallpapers.ru/index/page1/")
print(html.text)

session.close()