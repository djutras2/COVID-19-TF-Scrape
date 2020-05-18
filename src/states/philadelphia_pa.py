# # https://public.tableau.com/views/Covid-19-Demo/MappingDash?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=no&:animate_transition=no&:display_static_image=no&:display_spinner=no&:display_overlay=yes&:display_count=yes&:loadOrderID=6%22

# from selenium import webdriver
# from bs4 import BeautifulSoup
# import time
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import WebDriverException
# from datetime import datetime
# import os

# import csv

# from .state_helper import header, is_int, get_path, write_row

# def fetch_phil_pa():
#     location = "PHIL_PA.csv"

#     try:
#         url = 'https://public.tableau.com/views/Covid-19-Demo/MappingDash?:embed=y&:showVizHome=no&:host_url=https%3A%2F%2Fpublic.tableau.com%2F&:embed_code_version=3&:tabs=no&:toolbar=no&:animate_transition=no&:display_static_image=no&:display_spinner=no&:display_overlay=yes&:display_count=yes&:loadOrderID=6%22'

#         options = webdriver.ChromeOptions()
#         options.add_argument('--ignore-certificate-errors')
#         options.add_argument('--incognito')
#         options.add_argument('--headless')
#         options.add_argument("--disable-infobars")
#         driver = webdriver.Chrome("./chromedriver.exe", options=options)
        
#         driver.get(url)
        
#         # print(driver.page_source)

#         driver.implicitly_wait(10)

#         #iframe = driver.find_element_by_xpath('//*[@id="viz1587145247251"]/iframe')

#         canvas = driver.find_element_by_xpath('//*[@id="view7102796246370123014_2043762056387495646"]/div[1]/div[2]/canvas[2]')

#         driver.find_element_by_xpath('//*[@id="view7102796246370123014_2043762056387495646"]/div[5]')
        

#         # print(canvas.location)
#         # print(canvas.size)

#         dictionary = {}

#         driver.implicitly_wait(.1)
#         for y in range(50, canvas.size["height"] - 50, 10):
#             for x in range(50, canvas.size["width"] - 50, 10):
#                 # print(str(x) + ', ' + str(y))
#                 try:
#                     actions = webdriver.common.action_chains.ActionChains(driver)
#                     actions.move_to_element_with_offset(canvas, x, y)
#                     actions.perform()
#                 except:
#                     # print("Out of bounds...")
#                     break
#                 try:
#                     #code = driver.find_element_by_class_name('tab-ubertipToolTip')
#                     values = driver.find_elements_by_class_name("tab-selection-relaxation")
#                     if(dictionary.get(values[0].text) == None): 
#                         dictionary[values[0].text] = values[1].text
#                         # print("found " + values[0].text)
#                 except:
#                     continue
                
#         # table_html = table.get_attribute('innerHTML')

#         # date = driver.find_element_by_xpath('//*[@id="mobile-wrap"]/main/div[2]/div[2]/div[2]/p[2]').text
#         # date = date[len("*Updated weekly. Last updated "):-1]

#         # print(table_html)

#         driver.quit()

#     except WebDriverException as e:
#         print(url + " failed to load")
#         print(e)
#         driver.quit()
#         return None
    
#     # print(dictionary.items())

#     with open(os.path.join(get_path(), location), 'w', encoding='utf-8') as out:
#         writer = csv.writer(out)
#         writer.writerow(header)
#         for zipcode, cases in dictionary.items():
#             # writer.writerow([zipcode, cases, "N/A", datetime.date(datetime.now()), url])
#             write_row(writer, url, zipcode, cases)
# # fetch()
