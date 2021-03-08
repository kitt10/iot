from selenium import webdriver
import requests
import copy
import urllib.request
import time
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--headless')

# mac
# driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver')
# linux
driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=options)

URL = 'https://www.chmi.cz/predpovedi/predpovedi-pocasi/ceska-republika/kraje/plzensky'
driver.get(URL)

# a = soup.findAll('a')
driver.implicitly_wait(1)
results = driver.find_element_by_id('loadedcontent').text.split('\n\n')

# results = soup.find_all('div')
# print(results.prettify())
# print(results)
driver.close()
print(results[4])
print("comp")