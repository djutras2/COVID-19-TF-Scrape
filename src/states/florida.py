# https://www.arcgis.com/home/item.html?id=4fb81ffe99ef4ad49d12f1d2a2e75cf8#data

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import os

from .state_helper import get_path, extract_cases

def fetch_florida():
    location = "FL.csv"

    try:
        url = "https://www.arcgis.com/home/item.html?id=4fb81ffe99ef4ad49d12f1d2a2e75cf8#data"
        
        # print("trying " + url)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        driver.get(url)

        # all_source = driver.page_source

        delay = 20 # seconds
        try:
            # body = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dgrid_0"]/div[2]')))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dijit_layout_ContentPane_3"]/div[3]')))
            #print("Page is ready!")

            #all_source = driver.page_source


        except:
            print ("Loading took too much time!")
            return None
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        driver.implicitly_wait(20)
        driver.find_element_by_xpath('//*[@id="dgrid_0"]/div[2]')
        driver.execute_script('document.getElementsByClassName("dgrid-scroller")[0].scrollTo(0, 0)')
        
        florida_data = ""
        scroll_to = 0
        num_features = 1686

        for i in range(1, num_features):
            id = "dgrid_0-row-" + str(i)
            #print("searching for " + id)
            try:
                driver.implicitly_wait(5)
                row = driver.find_element_by_id(id)
            except:
                print("couldn't find " + id)
                continue
            scroll_to += row.size['height']
            driver.execute_script('document.getElementsByClassName("dgrid-scroller")[0].scrollTo(0,' + str(scroll_to) + ')')
            florida_data += row.get_attribute('innerHTML') + "\n\n"

        driver.quit()

        #return all_source
        soup = BeautifulSoup(florida_data, "html.parser")
    except WebDriverException as e:
        print(url + " failed to load")
        print(e)
        driver.quit()
        return None
   
    with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
        out.write("Zip Code, Confirmed COVID-19 Cases, Date, Source URL\n")

        for tag in soup.find_all("table"):
            zipcode = tag.find("td", {"class":"field-ZIP"})
            cases = tag.find("td", {"class":"field-Cases_1"})

            line = "%s, %s, %s, %s\n" % (zipcode.getText(), extract_cases(cases.getText()), datetime.date(datetime.now()), url)
            out.write(line)

# fetch_florida()