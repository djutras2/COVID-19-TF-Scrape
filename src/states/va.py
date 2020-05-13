from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException
import os
import time
import csv
from .state_helper import header, is_int, get_path, write_row

import tempfile
import slate3k as slate

def is_zip(string):
    if(is_int(string)):
        return len(string) == 5
    else:
        return string == "Not Report.." or string == "Out-of-State"

url = "https://public.tableau.com/views/VirginiaCOVID-19ZIPCodeDashboard/ZIPCodeTable?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=n&%3AbootstrapWhenNotified=false"
temp_dir = tempfile.gettempdir()

def scrape_pdf():
    # options = webdriver.ChromeOptions()
    # options.add_argument('--ignore-certificate-errors')
    # options.add_argument('--incognito')
    # options.add_argument('--headless')
    # options.add_argument("--disable-infobars")

    # prefs = {}
    # prefs["profile.default_content_settings.popups"]=0
    # prefs["download.default_directory"]=output_directory
    # options.add_experimental_option("prefs", prefs)

    # print(temp_dir)

    options = Options()
    options.add_argument("--disable-notifications")
    options.add_argument('--no-sandbox')
    options.add_argument('--verbose')
    options.add_experimental_option("prefs", {
        "download.default_directory": temp_dir,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing_for_trusted_sources_enabled": False,
        "safebrowsing.enabled": False
    })
    options.add_argument('--disable-gpu')
    options.add_argument('--disable-software-rasterizer')
    options.add_argument('--headless')

    driver = webdriver.Chrome("./chromedriver.exe", chrome_options=options)

    params = {'behavior': 'allow', 'downloadPath': temp_dir}
    driver.execute_cdp_cmd('Page.setDownloadBehavior', params)

    driver.get(url)

    driver.implicitly_wait(5)
    driver.find_element_by_xpath('//*[@id="download-ToolbarButton"]/span[1]').click()
    driver.find_element_by_xpath('//*[@id="DownloadDialog-Dialog-Body-Id"]/div/button[4]').click()
    download = driver.find_element_by_xpath('//*[@id="PdfDialog-Dialog-Body-Id"]/div/div[2]/div[4]/button')
    time.sleep(1)
    download.click()

    time.sleep(10)
    driver.close()

def fetch_virginia():
    # url = "https://public.tableau.com/views/VirginiaCOVID-19ZIPCodeDashboard/ZIPCodeTable?%3Aembed=y&%3AshowVizHome=no&%3Adisplay_count=y&%3Adisplay_static_image=n&%3AbootstrapWhenNotified=false"

    scrape_pdf()

    # creating a pdf file object 
    with open(os.path.join(temp_dir, 'ZIP Code Table.pdf'), 'rb') as pdfFileObj:
        pdf = slate.PDF(pdfFileObj, just_text=1, check_extractable=False)
        # print(pdf)

        zipcodes = []
        cases = []
        for i in pdf:
            i = i.replace("\t", " ").replace("\n", "\t")
            for j in i.split("\t"):
                j = j.strip()
                if(len(j) < 1):
                    continue
                # print(j)
                if(is_zip(j)):
                    zipcodes.append(j)
                elif(len(zipcodes) > len(cases)):
                    # print(j)
                    cases.append(j)

    with open(os.path.join(get_path(), "VA.csv"), 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(header)

        for z, c in zip(zipcodes, cases):
            if("*" in c):
                c = ""
            # out.write(z + ", " + c + "\n")
            write_row(writer, url, z, c)

    os.remove(os.path.join(temp_dir, 'ZIP Code Table.pdf'))