# https://coronavirus.maryland.gov/

from datetime import datetime

import os, sys

from src.url_helper import download_document
import csv

from .state_helper import header, is_int, get_path, write_row

def fetch_maryland():
    url = "https://opendata.arcgis.com/datasets/3e378abeb60748a8a8b92e29c14a86d0_0.csv"
    download_document(url, "MD_source.csv")

    with open("MD_source.csv","r") as source:
        reader = csv.reader(source)
        with open(os.path.join(get_path(), "MD.csv"),"w") as result:
            writer = csv.writer(result)
            writer.writerow(header)
            for row in reader:
                # if(is_int(row[1])):
                #     writer.writerow([row[1], extract_cases(row[3]), "", datetime.date(datetime.now()), "https://opendata.arcgis.com/datasets/3e378abeb60748a8a8b92e29c14a86d0_0.csv"])
                write_row(writer, url, row[1], row[3])
    
    os. remove("MD_source.csv")

