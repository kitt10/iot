from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import json
import time
import datetime

options = Options()
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--headless')

last_hour = 9999

while True:
    if datetime.datetime.now().hour != last_hour and datetime.datetime.now().minute in range(40,50):
        last_hour=datetime.datetime.now().hour
        # mac
        # driver = webdriver.Chrome(executable_path='/usr/local/bin/chromedriver',options=options)
        # linux
        driver = webdriver.Chrome(executable_path='/usr/bin/chromedriver',chrome_options=options)

        URL = 'https://www.chmi.cz/predpovedi/predpovedi-pocasi/ceska-republika/kraje/plzensky'
        # Stránka připravena 08.03.2021 v 16:01 UTC Swing a.s. Předpověď je vydávána 5xdenně v 5, 10:30, 12, 17 a 22 hodin
        driver.get(URL)

        # data = {}
        # data['output']=[]
        # with open("sample_file.json", "w") as file:
        #     json.dump(data, file)
        #
        # def job_function():
        #     with open("sample_file.json", "r+") as file:
        #         data = json.load(file)




        # results = driver.find_element_by_id('loadedcontent').text.split('\n\n')
        # driver.get_screenshot_as_file("screenshot.png")



        t = time.localtime()
        current_time = time.strftime("%H_%M_%S", t)
        print(current_time)

        S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
        driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment
        driver.find_element_by_tag_name('body').screenshot('web_screenshot_'+current_time+'.png')

        driver.close()

    time.sleep(30)




# print(results[4])
print("comp")