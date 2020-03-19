from selenium import webdriver
from time import sleep

import settings
from modules.crawl.get_link import get_link

accounts = []

def get_user_pass():
    with open(settings.ACCT_FILE, "r") as f:
        lines = f.readlines()
        f.close()

    i = 1
    for line in lines:
        if i != 2:
            acct = line
            i += 1
        else:
            password = line
            accounts.append({
                "user": acct,
                "pass": password
            })
            i -= 1    
        

def sign_in():
    get_user_pass()

    for account in accounts:
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.default_content_setting_values.notifications": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        chrome_options.add_argument("start-maximized")
        chrome_options.add_argument("start-maximized")
        driver = webdriver.Chrome(settings.CHROME_DRIVER, chrome_options=chrome_options)

        driver.get(settings.URL)
        sleep(3)

        # type user name and password to TextField
        driver.find_element_by_id('email').send_keys(account['user'].replace('\n', ''))
        sleep(3)
        driver.find_element_by_id('pass').send_keys(account['pass'].replace('\n', ''))
        sleep(3)
        
        driver.find_element_by_id('loginbutton').click()
        # driver.implicitly_wait(0.5)
        get_link(driver)        
