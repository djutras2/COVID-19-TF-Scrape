# https://www.stlouis-mo.gov/covid-19/data/zip.cfm

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

from .state_helper import header, is_int, get_path, write_row

def fetch_hamilton_oh():
    location = "HAM_OH.csv"

    try:
        url = 'https://www.hamiltoncountyhealth.org/covid-19-zip/'

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        options.add_argument("--disable-infobars")
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        driver.get(url)
        
        # print(driver.page_source)

        driver.implicitly_wait(10)

        # get table body
        table = driver.find_element_by_xpath('//*[@id="mobile-wrap"]/main/div[2]/div[2]/div[2]/table/tbody')

        table_html = table.get_attribute('innerHTML')

        date = driver.find_element_by_xpath('//*[@id="mobile-wrap"]/main/div[2]/div[2]/div[2]/p[2]').text
        date = date[len("*Updated weekly. Last updated "):-1]

        # print(table_html)

        driver.quit()

    except WebDriverException as e:
        print(url + " failed to load")
        print(e)
        driver.quit()
        return None
    
    soup = BeautifulSoup(table_html, "html.parser")

    with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(header)
        for tag in soup.find_all("tr"):
            tds = tag.find_all("td")
            zipcode = tds[0].getText().strip()
            cases = tds[1].getText().strip()
            # if(is_int(zipcode)):
            #     writer.writerow( [zipcode, extract_cases(cases), "N/A", date, url])
            write_row(writer, url, zipcode, cases)

# fetch()
