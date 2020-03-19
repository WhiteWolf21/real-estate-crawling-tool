from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options 
import pandas as pd 
import sys
import os

def main():

    chrome_options = Options()  
    # chrome_options.add_argument("--headless")    

    driver = webdriver.Chrome(executable_path='/home/whitewolf21/Documents/Gitlab/simple_crawl_links/chromedriver',   chrome_options=chrome_options) 
    driver.get("https://batdongsan.com.vn/nha-dat-ban")
    last_page = driver.find_elements_by_css_selector('div.background-pager-right-controls a')[-1].get_attribute("href")
    last_page = int(last_page.split("/p")[-1])

    for page in range(1,last_page+1):
        driver.get("https://batdongsan.com.vn/nha-dat-ban/p"+str(page))
        posts = driver.find_elements_by_css_selector('div.vip0.search-productItem')

        links = []
        for post in posts:
            # print(post.text)
            links.append(str(post.find_element_by_css_selector('a').get_attribute("href")))

        for link in links:
            driver.get(link)
            
        
        print("======================")
        print(page+1)
        print("======================")

if __name__ == "__main__":
    main()
