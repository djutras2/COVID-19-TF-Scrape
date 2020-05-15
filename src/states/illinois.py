# http://www.dph.illinois.gov/covid19/covid19-statistics

import os
import csv
import json

from src.url_helper import download_document
from .state_helper import header, is_int, get_path, write_row

def fetch_illinois():
    location = "IL.csv"
    source_file_temp = "IL_source.json"
    #address = 'http://www.dph.illinois.gov/covid19/covid19-statistics'
    url = "http://www.dph.illinois.gov/sitefiles/COVIDZip.json"
    
    download_document(url, source_file_temp)

    source_json = {}

    with open(source_file_temp) as source:
        source_json = json.load(source)

    # print(source_json["zip_values"])

    with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(header)

        date_record = source_json["LastUpdateDate"]
        date = str(date_record["year"]) + "-" + str(date_record["month"]) + "-" + str(date_record["day"]) 

        for record in source_json["zip_values"]:
            write_row(writer, url, record["zip"], record["confirmed_cases"], date=date)

    os.remove(source_file_temp)

    # try:
    #     #print("trying " + address)

    #     options = webdriver.ChromeOptions()
    #     options.add_argument('--ignore-certificate-errors')
    #     options.add_argument('--incognito')
    #     options.add_argument('--headless')
    #     options.add_argument("--disable-infobars")
    #     driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
    #     driver.get(address)

    #     driver.implicitly_wait(10)

    #     driver.find_element_by_xpath('//*[@id="content"]/article/div/div/div/ul[1]/li[2]/a').click()
    #     driver.find_element_by_xpath('//*[@id="pagin"]/li[46]/a').click()
    #     print(driver.find_element_by_link_text("All")).click()

    #     # date = driver.find_element_by_xpath('//*[@id="updatedDate"]').text

    #     # ensure last element has loaded

    #     driver.find_element_by_xpath('//*[@id="detailedData"]/tbody/tr[444]/td[1]')

    #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    #     table = driver.find_element_by_xpath('//*[@id="detailedData"]')

    #     table_html = table.get_attribute('innerHTML')

    #     # print(table_html)

    #     driver.quit()

    # except WebDriverException as e:
    #     print(address + " failed to load")
    #     print(e)
    #     driver.quit()
    #     return None
    
    # soup = BeautifulSoup(table_html, "html.parser")
    # with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
    #     writer = csv.writer(out)
    #     writer.writerow(header)

    #     for body in soup.find_all("tbody"):
    #         for row in body.find_all("tr"):
    #             tds = row.find_all("td")
    #             zipcode = tds[0]
    #             cases = tds[1]
    #             deaths = tds[2]

    #             write_row(writer, address, zipcode.getText(), cases.getText(), deaths=deaths.getText())

# fetch_illinois("http://www.dph.illinois.gov/covid19/covid19-statistics")
