from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
import datetime
import random

START = "http://oreilly.com"
random.seed(datetime.datetime.now())

def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks
            
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #Finds all links that start with "http" or "www" that do
    #not contain the current URL
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def getRandomExternalLink(startingPage):
    try:
        html = urlopen(startingPage)
        bsObj = BeautifulSoup(html, "html.parser")
        externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
        if len(externalLinks) == 0:
            internalLinks = getInternalLinks(bsObj, startingPage)
            return getRandomExternalLink(internalLinks[random.randint(0, len(internalLinks) - 1)])
        else:
            return externalLinks[random.randint(0, len(externalLinks) - 1)]
    except:
        print("ouch!")
        return START
    
def followExternalOnly(starting_site):
    external_link = getRandomExternalLink(starting_site)
    print("Random external link is: "+external_link)
    followExternalOnly(external_link)

followExternalOnly(START)
