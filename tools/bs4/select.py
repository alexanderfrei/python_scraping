import urllib.request
from bs4 import BeautifulSoup
import re

# select by class

html = urllib.request.urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
bsObj = BeautifulSoup(html, "html.parser")
nameList = bsObj.findAll("span", {"class":"green"}) # tag, css {attr: value} - python dictionary
result_list = [name.get_text() for name in nameList] # get_text()
# print(result_list)

# select by attribute

allText = bsObj.findAll(id="text")
# print(allText[0].get_text()[:100])

# syntax tree

html = urllib.request.urlopen("http://www.pythonscraping.com/pages/page3.html")
bsObj = BeautifulSoup(html, "html.parser")
gift_table = bsObj.findAll("tr",{"class":"gift", }) # get ResultSet

for gift in gift_table:
    [gc for gc in gift.children] # get list of children
    gift.find('td').get_text() # iterating by ResultSet and get first td - name of gift

for sibling in bsObj.find("table",{"id":"giftList"}).tr.next_siblings:
    sibling # next_siblings return all siblings except first

print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())

# regular expressions

images = bsObj.findAll("img", {"src":re.compile("\.\.\/img\/gifts/img.*\.jpg")})
for image in images:
    print(image["src"])

# get attributes of tag / attrs

print([image.attrs['src'] for image in images])

# lambda functions

html = urllib.request.urlopen("http://www.pythonscraping.com/pages/page2.html")
bsObj = BeautifulSoup(html, "html.parser")
tags = bsObj.findAll(lambda tag: len(tag.attrs) == 2) # use function to parse tag
for tag in tags:
	print(tag)

