#!/usr/bin/python
"""
@Author Hayden M Nier
Opens the top posts from r/wallpaper and r/wallpapers and saves all of the images.

No gaurantees if you use this script yada yada yada
"""
import sys
import urllib
import urlparse
import requests
from bs4 import BeautifulSoup
import itertools
import code
#code.interact(local=locals())
 
"""
Takes lists of links and downloads them using urlretrieve
"""
def getFlics(links):
    for l in links:
        l = urlparse.urljoin("https://",l)
        x = urlparse.urlparse(l)
        if '/a/' not in x.path and ( ("jpg" in x.path) or ("png" in x.path) ):
            print(x.path)
            url = x.path.split(")")[0][1:] #get rid of / and make sure there are no rando )'s
            urllib.urlretrieve(l,"../Images/"+url)
        else:
            print(l + " is an album")
            getPage(l,"album")


"""
Creates a session and gets the page. Parses the page based on whether it is an imgur album or a reddit page.
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
            if x:
                parsedX = urlparse.urlparse(x)
                if pageType=="reddit":
                    if "imgur" in x and x not in links and "domain" not in x and '/r' not in x: 
                        links.append(x)
                if pageType=="album":
                    if "imgur" in x and x not in links and ("jpg" in x or "png" in x): 
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
    url = "https://www.reddit.com/r/EarthPorn/top/?sort=top&t=day"
    getPage(url,"reddit")

main()
