import socks
import socket
import requests
from bs4 import BeautifulSoup
import re

START_PAGE = "http://r-analytics.blogspot.ru/"

####################################################
# configuring requests session

headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    'Connection': 'keep-alive'
}

session = requests.Session()
socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
session.headers = headers
socket.socket = socks.socksocket

##  test
# ip_test = session.get('http://ipinfo.io/ip')
# print(ip_test.text, session.headers)

####################################################

with open('./posts.txt','w') as file:
    pass

def crawl_page(page_url):

    url = session.get(page_url)
    bsObj = BeautifulSoup(url.text, "html.parser")
    posts = bsObj.findAll("div", {"class":"post hentry"})

    for post in posts:
        comment = post.find("a", {"class":"comment-link"})
        comment_num = int(comment.get_text().replace('коммент.',''))
        if comment_num > 2:
            header = post.find("h3", class_=re.compile("post-title.*")).find('a')
            with open('./posts.txt','a') as file:
                file.write(" ".join([re.sub('\\n','',header.get_text()), header.attrs['href'], '\n']))

    older_page = bsObj.find("a", {"class":"blog-pager-older-link"})
    try:
        crawl_page(older_page.attrs['href'])
    except:
        pass

crawl_page(START_PAGE)
session.close()

