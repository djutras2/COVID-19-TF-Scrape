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

from arcgis.gis import GIS
from arcgis.features import FeatureLayer

from .state_helper import header, get_path, write_row

import csv

def fetch_florida():
    location = "FL.csv"
    url = "https://services1.arcgis.com/CY1LXxl9zlJeBuRZ/ArcGIS/rest/services/Florida_Cases_Zips_COVID19/FeatureServer/0"

    layer = FeatureLayer(url)
    query = layer.query(out_fields='ZIP,Cases_1')
    
    with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(header)

        for feature in query.features:
            write_row(writer, url, feature.get_value('ZIP'), feature.get_value('Cases_1'))