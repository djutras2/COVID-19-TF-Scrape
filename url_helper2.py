from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from url_helper import get_url_root
import os

# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25

def get_soup_from(address):
    '''
    Returns a BeautifulSoup object from the contents at this address. To replace url_helper.get_soup_from

    Example:
    - get_soup_from("https://ready.alaska.gov/covid19")
    - get_soup_from(HD_PATH + "Alabama Department of Public Health.html")

    Parameters:
    - address -- a file or url
    '''
    if(get_url_root(address) == None):
        if os.path.isfile(address):
            return BeautifulSoup(open(address, errors='ignore'), "html.parser")
        else:
            return None

    try:

        options = webdriver.ChromeOptions()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--incognito')
        options.add_argument('--headless')
        driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
        #driver.implicitly_wait(30)
        driver.get(address)

        all_source = driver.page_source
        iframes = driver.find_elements_by_tag_name(("iframe"))

        for frame in iframes:
            driver.switch_to.frame(frame)
            all_source += "\n" + driver.page_source
            driver.switch_to.default_content()

        # try:
        #     element = WebDriverWait(driver, 10).until(
        #     EC.presence_of_element_located((By.PARTIAL_LINK_TEXT, ("leaflet")))
        #     )
        # finally:
        #     driver.quit()

        # wait = WebDriverWait(driver, 100)

        # wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, '.leaflet-popup-content b')))

        # popup = driver.find_element_by_class_name("leaflet-popup-content")

        # print(popup)

        #element = driver.find_element_by_xpath('//a[contains(@href,"leaflet")]')
        # print(element)

        driver.quit()

        return BeautifulSoup(all_source, "html.parser")
    except:
        return None

### Test ###
#bs = fetch("https://coronavirus.utah.gov/case-counts")
# with open("selenium_test.txt", 'w', encoding='utf-8') as out:
#     out.write(bs.getText())
# print("leaflet" in bs.getText().lower())