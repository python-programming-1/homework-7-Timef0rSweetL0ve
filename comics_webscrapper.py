# Homework 7
# Write a python program that will download the latest 10 comic images from https://www.gocomics.com/pearlsbeforeswine/
# Navigate to the latest page by clicking 'Read More'.

import requests
import bs4
import os
import re

url = 'https://www.gocomics.com/pearlsbeforeswine/2019/08/20'
for i in range(10):
    res = requests.get(url)   # download web page to save into res obj.
    res.raise_for_status()    # check for a successful download.

    # create BeautifulSoup object to store html source code as .txt file
    code_text = bs4.BeautifulSoup(res.text, "html.parser")
    comic_image = code_text.select('a[itemprop="image"]')   # find the specific image of the current comic using <a> tag

    # find specific image url
    picture_elm = comic_image[0].contents[1]     # return <picture> tag as contents
    for img in picture_elm:
        image_url = img['src'] + '.png'          # return a url with attribute 'src' within <img> tag
    image_res = requests.get(image_url)          # download the image url and store in image_res obj.
    image_res.raise_for_status()                 # return 200 for a successful url download

    # save image url
    image_file = open(os.path.basename(image_url), 'wb')   # open the file in write binary mode by passing 'wb' in the second argument
    for chunk in res.iter_content(100000):    # each chunk of 100000 bytes returned from each iteration
        image_file.write(chunk)               # write() returns the number of bytes as chunk written into image_file
    image_file.close()

    # get previous url
    prev_link = code_text.select('nav[role="group"]')[0].contents[1]       # return <div > tag that contains <a> subtag
    for a_tag in prev_link:             # return each <a > for each iteration
        prev_comic = re.compile(r'js-previous-comic').findall(str(a_tag))  # using regex to find specific term associated with one-step previous button
        if prev_comic:
            url = 'https://www.gocomics.com' + a_tag.get('href')           # if the term is found, print the related 'href'
            print(url)
