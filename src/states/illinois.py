# http://www.dph.illinois.gov/covid19/covid19-statistics

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from datetime import datetime
import os

from .state_helper import header, get_path, extract_cases

def fetch_illinois():
    location = "IL.csv"
    address = 'http://www.dph.illinois.gov/covid19/covid19-statistics'
    
    try:
        #print("trying " + address)

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        driver.get(address)
        
        # print(driver.page_source)

        driver.implicitly_wait(10)

        driver.find_element_by_xpath('//*[@id="pagin"]/li[38]/a').click()

        driver.find_element_by_xpath('//*[@id="content"]/article/div/div/div/ul[1]/li[2]/a').click()

        date = driver.find_element_by_xpath('//*[@id="updatedDate"]').text

        # ensure last element has loaded
        driver.implicitly_wait(15)
        driver.find_element_by_xpath('//*[@id="detailedData"]/tbody/tr[369]/td[1]')

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

        table = driver.find_element_by_xpath('//*[@id="detailedData"]')

        table_html = table.get_attribute('innerHTML')

        # print(table_html)

        driver.quit()

    except WebDriverException as e:
        print(address + " failed to load")
        print(e)
        driver.quit()
        return None
    
    soup = BeautifulSoup(table_html, "html.parser")
    with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
        out.write("Zip Code, Confirmed COVID-19 Cases,  Confirmed COVID-19 Deaths, Date, Source URL\n")
        for body in soup.find_all("tbody"):
            for row in body.find_all("tr"):
                tds = row.find_all("td")
                zipcode = tds[0]
                cases = tds[1]
                deaths = tds[2]

                line = "%s, %s, %s, %s, %s\n" % (zipcode.getText(), extract_cases(cases.getText()), deaths.getText(), date, address)
                out.write(line)

# fetch_illinois("http://www.dph.illinois.gov/covid19/covid19-statistics")
