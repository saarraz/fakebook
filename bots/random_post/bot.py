# -*- coding: utf-8 -*-

import random
import requests
import model
from bots.post_bot import PostBot
import socket
import sys
from selenium import webdriver
from PIL import Image
from googletrans import Translator
from bs4 import BeautifulSoup
from selenium.webdriver.common.keys import Keys
import os

def RndNameMale():
    k = BeautifulSoup(requests.get('https://www.behindthename.com/random/random.php?number=2&gender=m&surname=&norare=yes&all=yes').content)
    k = [x.text for x in k.findAll(attrs={'class': 'plain'})]
    i=0
    klk =""
    while i<2:
        klk+= k[i]+ " "
        i+=1
    print(klk)

def RndNameFemale():
    k = BeautifulSoup(requests.get('https://www.behindthename.com/random/random.php?number=2&gender=f&surname=&norare=yes&all=yes').content)
    k = [x.text for x in k.findAll(attrs={'class': 'plain'})]
    i=0
    klk =""
    while i<2:
        klk+= k[i]+ " "
        i+=1
    print(klk)


class RandomUserPostBot(object):

    IMAGE_COMMENTS = [
        'חחחחחחחחחחחחחחחח',
        'כל כך נכון. {good_day}',
        'גורם לך לחשוב. {good_day}',
        'מדהיםםםם!!! {good_day}',
        '{good_day}'
    ]

    GOOD_DAY = [
        'יום טוב',
        'יום טוב אנשים',
        'בוקר טוב',
        'גוד ווייבססס'
    ]

    def generate(self, user, when):
        if random.random() > .5:
            driver = webdriver.Chrome(r'chromedriver')
            driver.get('https://tomforth.co.uk/guardiancomments/')
            comment = driver.find_element_by_class_name('commentBody')
            comment = Translator().translate(comment.text, dest='he')
            driver.close()
            return model.Post(when, comment, None, user)
        else:
            image = requests.get(requests.get('http://inspirobot.me/''api?generate=true').content).content
            path = os.path.join(model.IMAGE_DIR, '{}.jpg'.format(str(random.randint(0, 0xffffffff))))
            open(path, 'wb').write(image)
            return model.Post(when, random.choice(self.IMAGE_COMMENTS).format(good_day=random.choice(self.GOOD_DAY)),
                              model.Image(path), user)