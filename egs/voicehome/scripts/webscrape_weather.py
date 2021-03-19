from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import datetime
import re

options = Options()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--headless')

# last_hour = 9999
#
# while True:
#     if datetime.datetime.now().hour != last_hour and datetime.datetime.now().minute in range(40,50):

# mac
driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=options)
# linux
# driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=options)

# Předpověď je vydávána 5xdenně v 5, 10:30, 12, 17 a 22 hodin
URL = 'https://www.chmi.cz/predpovedi/predpovedi-pocasi/ceska-republika/kraje/plzensky'

driver.get(URL)

# data = {}
# data['output']=[]
# with open("sample_file.json", "w") as file:
#     json.dump(data, file)
#
# def job_function():
#     with open("sample_file.json", "r+") as file:
#         data = json.load(file)




results = driver.find_element_by_id('loadedcontent').text.split('\n\n')

driver.close()

regex_patterns_forecast_today = [
    '^(Počasí dnes večer a v noci \(18-07\))',
    '^(Počasí \(12-22\))',
    '^(Počasí \(06-22\))'
]

breaker = False
for num_line in range(2,8):
    for pattern in regex_patterns_forecast_today:
        match = re.search(pattern, results[num_line])
        if match:
            forecast_today = match.string.split('\n')[1]
            break
    if breaker:
        break


regex_patterns_forecast_tomorrow = '^(Počasí přes den \(07-24\))'

for num_line in range(4,8):
    match = re.search(regex_patterns_forecast_tomorrow, results[num_line])
    if match:
        forecast_tomorrow = match.string.split('\n')[1]
        break


# print(results[4])
print("comp")