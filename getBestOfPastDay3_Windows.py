#!/usr/bin/python3
"""
@Author Hayden M Nier
Opens the top posts from r/wallpaper and r/wallpapers and saves all of the images.

No gaurantees if you use this script yada yada yada

Pip Install List:
pip install bs4
pip install requests
pip install image
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
Added by David Masse for purposes of changing Windows Desktop Wallpaper
"""
import ctypes
import os
import shutil
import random
from PIL import Image
import subprocess

#Used for the path of where pictures should be saved based off of the user
user_name = os.getenv("username")
full_path = "C:\\Users\\" + user_name + "\\Pictures\\RedditWallpaper\\"
bmp_path = full_path + "BMP\\"

"""
Sets desktop background for Windows OSError
Author: David Masse
"""

def setWallpaper():
    if not os.path.exists(bmp_path):
        os.makedirs(bmp_path)
    else:
        shutil.rmtree(bmp_path)
        os.makedirs(bmp_path)

    image_path = random.choice(os.listdir(full_path))

    file_in = full_path + image_path
    img = Image.open(file_in)

    file_out = bmp_path + image_path + ".bmp"
    img.save(file_out)

    batcmd1 = ("reg add \"HKCU\\Control Panel\\Desktop\" /v WallPaper /t REG_SZ /d  \"" + bmp_path + image_path + ".bmp\"" + " /f")
    result1 = subprocess.check_output(batcmd1, shell=True)
    batcmd2 = ("RUNDLL32.EXE user32.dll,UpdatePerUserSystemParameters")
    result2 = subprocess.check_output(batcmd2, shell=True)

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
            urllib.request.urlretrieve(l,full_path + url)
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
    if not os.path.exists(full_path):
        os.makedirs(full_path)
    else:
        shutil.rmtree(full_path)
        os.makedirs(full_path)
        
    url = "https://www.reddit.com/r/wallpaper+wallpapers/top/?sort=top&t=day"  
    getPage(url,"reddit")
    url = "https://www.reddit.com/r/EarthPorn/top/?sort=top&t=day"
    getPage(url,"reddit")
    setWallpaper()

main()
