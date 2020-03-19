from selenium.webdriver.common.keys import Keys
from re import search
from time import sleep
from random import seed
from random import random

import settings
from modules.crawl.crawl_comm import crawl_comm

re_mogi = r"mogivietnam"

# re_mogi = r"nhadattayninhgiare"

def random_waiting(min, max):
    return min + (random() * (max - min))

def get_link(signin_driver):
    seed(342)

    signin_driver.get(settings.GROUP)
    body = signin_driver.find_element_by_tag_name('body')

    for i in range(10):
        body.send_keys(Keys.ESCAPE) #close popup        

    for i in range(settings.SCROLLS):
        body.send_keys(Keys.PAGE_DOWN)
        body.send_keys(Keys.ESCAPE)
        if i % 8 == 0:
            sleep(random_waiting(0.3, 0.6))

    posts_link = []
    classes = signin_driver.find_elements_by_xpath('//*[@class="_5pcq"]')
    for c in classes:
        link = c.get_attribute('href')
        if search(pattern=re_mogi, string=link) is None:
            continue
        else:
            posts_link.append(link)
    # posts_link.append('https://www.facebook.com/groups/mogivietnam/permalink/2335039689865074/')
    #https://www.facebook.com/groups/mogivietnam/permalink/2335039689865074/
    # print(posts_link)
    crawl_comm(signin_driver, posts_link)
    