# https://coronavirus.maryland.gov/

from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from datetime import datetime

import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from url_helper import download_document
import csv

from state_helper import header

def fetch_maryland():
    download_document("https://opendata.arcgis.com/datasets/3e378abeb60748a8a8b92e29c14a86d0_0.csv", "MD_source.csv")

    with open("MD_source.csv","r") as source:
        reader = csv.reader(source)
        with open("MD.csv","w") as result:
            writer = csv.writer(result)
            writer.writerow(header)
            for row in reader:
                writer.writerow([row[1], row[3], "N/A", datetime.date(datetime.now()), "https://opendata.arcgis.com/datasets/3e378abeb60748a8a8b92e29c14a86d0_0.csv"])
    os. remove("MD_source.csv")

    #soup = BeautifulSoup(table_html, "html.parser")
    # with open("MD.csv", 'w', encoding='utf-8') as out:
    #     out.write(test)
    #    out.write("Zip Code, Confirmed COVID-19 Cases,  Confirmed COVID-19 Deaths, Date, Source URL\n")
    #     for body in soup.find_all("tbody"):
    #         for row in body.find_all("tr"):
    #             tds = row.find_all("td")
    #             zip = tds[0]
    #             cases = tds[1]
    #             deaths = tds[2]

    #             line = "%s, %s, %s, %s, %s\n" % (zip.getText(), cases.getText(), deaths.getText(), date, 'https://coronavirus.maryland.gov/')
    #             out.write(line)

fetch_maryland()
