# https://sc-dhec.maps.arcgis.com/home/item.html?id=1ae9ce8e3b8e4640abeb1e13a730207b#data

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import os
import csv

from .state_helper import header, get_path

def fetch_sc():
    try:
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        url = 'https://sc-dhec.maps.arcgis.com/home/item.html?id=1ae9ce8e3b8e4640abeb1e13a730207b#data'

        driver.get(url)

        driver.implicitly_wait(10)

        # switch to zipcode
        driver.find_element_by_xpath('//*[@id="esri_Evented_0"]/div[1]/div/div[1]/label/select').click()
        driver.find_element_by_xpath('//*[@id="esri_Evented_0"]/div[1]/div/div[1]/label/select/option[2]').click()
        

        # print(driver.page_source)

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        driver.implicitly_wait(20)

        # make sure scroller exists
        driver.find_element_by_xpath('//*[@id="dgrid_0"]/div[2]')
        driver.execute_script('document.getElementsByClassName("dgrid-scroller")[0].scrollTo(0, 0)')
        
        data = ""
        scroll_to = 0
        num_features = 388 # TODO: fetch this from site

        driver.implicitly_wait(5)
        for i in range(1, num_features):
            id = "dgrid_1-row-" + str(i)
            #print("searching for " + id)
            try:
                row = driver.find_element_by_id(id)
            except:
                print("couldn't find " + id)
                continue
            scroll_to += row.size['height']
            driver.execute_script('document.getElementsByClassName("dgrid-scroller")[0].scrollTo(0,' + str(scroll_to) + ')')
            data += row.get_attribute('innerHTML') + "\n\n"

        date_updated_element = driver.find_element_by_xpath('//*[@id="esri_Evented_0"]/div[2]/div[2]')
        date_updated = " ".join(date_updated_element.text.split()[3:6]).replace(",", "")

        driver.quit()

        #return all_source
    except WebDriverException as e:
        print(e)
        driver.quit()
        return None

    soup = BeautifulSoup(data, "html.parser")
    with open(os.path.join(get_path(), "SC.csv"), 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(header)
        for tag in soup.find_all("tr"):
            zips = tag.find("td", {"class":"field-POSTCODE"})
            deaths = tag.find("td", {"class":"field-Death"})
            cases = tag.find("td", {"class":"field-Positive"})

            writer.writerow([zips.getText(), cases.getText(), deaths.getText(), date_updated, url])