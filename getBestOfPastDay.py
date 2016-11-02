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
#code.interact(local=locals())
 
"""
Takes lists of links and downloads them using urlretrieve
"""
def getFlics(links):
    for l in links:
        x = urllib.parse.urlparse(l)
        url = x.path.split(")")[0][1:] #get rid of / and make sure there are no rando )'s
        print(url)
        urllib.request.urlretrieve(l,"../Images/"+url)


"""
Takes a Requests page, turns it into a Soup and creates a list of imgur jpg links
"""
def parsePage(page):
    links = []
    webPage = str(page.content) 
    mySoup = BeautifulSoup(webPage,'html.parser')
    for aTag in mySoup.find_all('a'):
        x = aTag.get('href')
        if x and "imgur" in x and "jpg" in x and x not in links:
            links.append(x)
    getFlics(links)

"""
Creates session with reddit using a specified User-agent and gets the page of today's top posts
"""
def main():
    url = "https://www.reddit.com/r/wallpaper+wallpapers/top/?sort=top&t=day"  
    sesh = requests.Session()
    page = sesh.get(url,headers={'User-agent':'ScendantWallpaperFinder'}) #need to specify my user agent 
    if page.status_code == 200:
        parsePage(page)
    else:
        print("Response was "+str(page.status_code))
main()
