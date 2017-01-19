from urllib.request import urlopen
from bs4 import BeautifulSoup

html = urlopen("http://www.pythonscraping.com/pages/warandpeace/chapter1-ru.txt")
bsObj = BeautifulSoup(html, "html.parser") # bs.get_text return text in unicode by default?
content = bsObj.get_text()
# content = bytes(content, "UTF-8")
# content = content.decode("UTF-8")
print(content)

# check  <META charset="utf-8" />
