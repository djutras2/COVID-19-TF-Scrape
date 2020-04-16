# https://www.arcgis.com/home/item.html?id=4fb81ffe99ef4ad49d12f1d2a2e75cf8#data

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime
import os

def get_soup_from(address):
    try:
        print("trying " + address)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        driver.get(address)

        all_source = driver.page_source

        delay = 20 # seconds
        try:
            # body = WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dgrid_0"]/div[2]')))
            WebDriverWait(driver, delay).until(EC.presence_of_element_located((By.XPATH, '//*[@id="dijit_layout_ContentPane_3"]/div[3]')))
            print("Page is ready!")

            all_source = driver.page_source


        except:
            print ("Loading took too much time!")
            return None
        
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        driver.implicitly_wait(20)
        scroller = driver.find_element_by_xpath('//*[@id="dgrid_0"]/div[2]')
        driver.execute_script('document.getElementsByClassName("dgrid-scroller")[0].scrollTo(0, 0)')
        # driver.execute_script('define("esri/tasks/support/nls/pbfDeps_en-us",{"esri/layers/vectorTiles/nls/common":{_localized:{}}});')
        
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
        return BeautifulSoup(florida_data, "html.parser")
    except RuntimeError as e:
        print(address + " failed to load")
        print(e)
        driver.quit()
        return None

## Test ###
soup = get_soup_from("https://www.arcgis.com/home/item.html?id=4fb81ffe99ef4ad49d12f1d2a2e75cf8#data")
# if(soup == None):
#     print("failed")
# else:
#     with open("florida_test.txt", 'w', encoding='utf-8') as out:
#         out.write(str(time.time()))
#         out.write(str(soup))

with open("FL.csv", 'w', encoding='utf-8') as out:
    out.write("Zip Code, Confirmed COVID-19 Cases, Date, Source URL\n")

    for tag in soup.find_all("table"):
        zip = tag.find("td", {"class":"field-ZIP"})
        cases = tag.find("td", {"class":"field-Cases_1"})

        line = "%s, %s, %s, %s\n" % (zip.getText(), cases.getText(), datetime.date(datetime.now()), "https://www.arcgis.com/home/item.html?id=4fb81ffe99ef4ad49d12f1d2a2e75cf8#data")
        out.write(line)