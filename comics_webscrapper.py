# Homework 7
# Write a python program that will download the latest 10 comic images from https://www.gocomics.com/pearlsbeforeswine/
# Navigate to the latest page by clicking 'Read More'.

import requests
import bs4
import os

url = 'https://www.gocomics.com/pearlsbeforeswine/2019/08/21'
for i in range(10):
    res = requests.get(url)   # download web page to save into res obj.
    res.raise_for_status()    # check for a successful download.

    # create BeautifulSoup object to store html source code as .txt file
    code_text = bs4.BeautifulSoup(res.text, "html.parser")

    # find specific image url
    img_tag = code_text.select('a[itemprop="image"]')[0].contents[1].contents[0]  # trace down the tree structure to get <img> tag
    image_url = img_tag.attrs['src']                                              # get attribute 'src' as link
    title_url = img_tag.attrs['alt']                                              # get attribute 'alt' as title
    image_res = requests.get(image_url)                                           # download the image url and store in image_res obj.
    image_res.raise_for_status()                                                  # return 200 for a successful url download

    # save image url
    image_file = open(title_url + '.png', 'wb')            # open the file in write binary mode by passing 'wb' in the second argument
    for chunk in image_res.iter_content(100000):           # each chunk of 100000 bytes of image_res returned from each iteration
        image_file.write(chunk)                            # write() returns the number of bytes as chunk written into image_file
    image_file.close()

    # get previous url
    prev_link = code_text.select('nav[role="group"]')[0].contents[1].contents[3].attrs['href']
    url = 'https://www.gocomics.com' + prev_link
    print('Previous page ' + str(int(i+1)) + ' is: ' + url)
