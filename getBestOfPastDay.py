#!/usr/bin/python3
"""
@Author Hayden M Nier
Opens the top posts from r/wallpaper and r/wallpapers and saves all of the images.

No gaurantees if you use this script yada yada yada
"""
import sys
import urllib.request
import urllib.parse
import requests
from bs4 import BeautifulSoup
import itertools
import http.client
import code
#code.interact(local=locals())
 
"""
Takes lists of links and downloads them using urlretrieve
"""
def getFlics(links):
    for l in links:
        l = urllib.parse.urljoin("https://",l)
        x = urllib.parse.urlparse(l)
        if '/a/' not in x.path and ( ("jpg" in x.path) or ("png" in x.path) ):
            print(x.path)
            url = x.path.split(")")[0][1:] #get rid of / and make sure there are no rando )'s
            urllib.request.urlretrieve(l,"../Images/"+url)
        else:
            print(l + " is an album")
            getPage(l,"album")


"""
Creates a session and gets the page. Calls parsePage if HTTP OK response
"""
def getPage(url,pageType):
    sesh = requests.Session()
    page = sesh.get(url,headers={'User-agent':'ScendantWallpaperFinder'}) #need to specify my user agent 
    if page.status_code == 200:
        links = []
        webPage = str(page.content) 
        mySoup = BeautifulSoup(webPage,'html.parser')
        for aTag in mySoup.find_all('a'):
            x = aTag.get('href')
            parsedX = urllib.parse.urlparse(x)
            if pageType=="reddit":
                if x and "imgur" in x and x not in links and "domain" not in x and '/r' not in x: 
                    links.append(x)
            if pageType=="album":
                if x and "imgur" in x and x not in links and ("jpg" in x or "png" in x): 
                    links.append(x)
        getFlics(links)
    else:
        print("Response was "+str(page.status_code))


"""
Sets url and calls get page
"""
def main():
    url = "https://www.reddit.com/r/wallpaper+wallpapers/top/?sort=top&t=day"  
    getPage(url,"reddit")


main()
