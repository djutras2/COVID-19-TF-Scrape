# https://oakgov.maps.arcgis.com/apps/opsdashboard/index.html#/462154e746b04af884c548111eccee73 

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

from .state_helper import header, is_int, get_path

def fetch_oakland_mi():
    location = "OAK_MI.csv"

    try:
        url = 'https://oakgov.maps.arcgis.com/apps/opsdashboard/index.html#/462154e746b04af884c548111eccee73'
        
        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        driver.get(url)
        
        # print(driver.page_source)

        driver.implicitly_wait(10)

        canvas = driver.find_element_by_xpath('//*[@id="esri.Map_0_gc"]')


        driver.implicitly_wait(20)

        zipcode_layer = driver.find_element_by_xpath('//*[@id="COVID19_Cases_by_Zip_Code_Total_Population_2441_layer"]')
        zipcode_objects = zipcode_layer.find_elements_by_tag_name("path")
        
        # print(len(zipcode_objects))

        # return None

        if(canvas == None):
            return

        # print(canvas.location)
        # print(canvas.size)

        dictionary = {}

        driver.implicitly_wait(.1)
        for zipcode_object in zipcode_objects:
            webdriver.common.action_chains.ActionChains(driver).move_to_element_with_offset(zipcode_object, zipcode_object.size["width"] / 2, zipcode_object.size["height"] / 2).click(zipcode_object).perform()
            try:
                # box popped up?
                box = driver.find_element_by_class_name('info-panel')
                #print(box)
                
                zipcode =  box.find_element_by_class_name('avenir-bold').text
                # print(zipcode)
                #table =  box.find_element_by_tag_name('table')

                cases = box.find_element_by_xpath('//table/tbody/tr[1]/td[2]/span').text
                deaths = box.find_element_by_xpath('//table/tbody/tr[2]/td[2]/span').text

                if(dictionary.get(zipcode) == None): 
                    dictionary[zipcode] = (cases, deaths)
                    # print("found " + zipcode)
                    
                # exit box
                box.find_element_by_xpath('div[2]/div[1]/div[2]/a/span/svg').click()
            except:
                continue

        driver.quit()

    except WebDriverException as e:
        print(url + " failed to load")
        print(e)
        driver.quit()
        return None
    
    # print(dictionary)

    if(dictionary != None):
        with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
            writer = csv.writer(out)
            writer.writerow(header)
            for zipcode, cases in dictionary.items():
                writer.writerow([zipcode, cases[0], cases[1], datetime.date(datetime.now()), url])

# fetch()
