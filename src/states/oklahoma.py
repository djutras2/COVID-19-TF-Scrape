from datetime import datetime
import os, sys
from src.url_helper import download_document
import csv
from .state_helper import header, is_int, get_path, write_row

def fetch_oklahoma():
    url = "https://storage.googleapis.com/ok-covid-gcs-public-download/oklahoma_cases_zip.csv"
    source_name = "OK_source.csv"
    download_document(url, source_name)

    with open(source_name,"r") as source:
        reader = csv.reader(source)
        with open(os.path.join(get_path(), "OK.csv"),"w") as result:
            writer = csv.writer(result)
            writer.writerow(header)
            for row in reader:
                # if(is_int(row[1])):
                #     writer.writerow([row[1], extract_cases(row[3]), "", datetime.date(datetime.now()), "https://opendata.arcgis.com/datasets/3e378abeb60748a8a8b92e29c14a86d0_0.csv"])
                write_row(writer, url, row[0], row[1], deaths=row[2], date=row[4].replace("/","-"))
    
    os.remove(source_name)

