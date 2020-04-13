from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# https://medium.com/ymedialabs-innovation/web-scraping-using-beautiful-soup-and-selenium-for-dynamic-page-2f8ad15efe25

def fetch(url):
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Chrome("./chromedriver.exe", options=options)
    
    #driver.implicitly_wait(30)

    driver.get(url)

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

    iframes = driver.find_elements_by_tag_name(("iframe"))
    print(iframes)
    all_source = driver.page_source

    for frame in iframes:
        driver.switch_to.frame(frame)
        all_source += "\n" + driver.page_source
        driver.switch_to.default_content()
    #element = driver.find_element_by_xpath('//a[contains(@href,"leaflet")]')
    # print(element)


    return BeautifulSoup(all_source, "html.parser")

bs = fetch("https://coronavirus.utah.gov/case-counts")

with open("selenium_test.txt", 'w', encoding='utf-8') as out:
    out.write(bs.getText())
print("leaflet" in bs.getText().lower())