from bs4 import BeautifulSoup as bs
from urllib.request import (
    urlopen, urlretrieve)
import os

def main(url, out_folder="./test/", alt=""):
    """Downloads all the images at 'url' to /test/"""
    soup = bs(urlopen(url), "lxml")
    if not (os.path.exists(out_folder)):
        os.mkdir(out_folder)
    img1 = soup.find("a", class_="image image-thumbnail")
    img = img1.find("img")
    print("Image: %(data-src)s" % img)
    filename = img['data-image-name']
    outpath = os.path.join(out_folder, filename)
    if img["data-src"].lower().startswith("http"):
        urlretrieve(img["data-src"], outpath)
    else:
        pass
