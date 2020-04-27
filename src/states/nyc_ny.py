# New York City

from datetime import datetime

import os, sys

# sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.url_helper import download_document
import csv

from .state_helper import header, is_int, get_path, write_row

def fetch_nyc():
    location = "NYC_NY"
    location_source = location + "_source"
    ext = ".csv"
    url = 'https://raw.githubusercontent.com/nychealth/coronavirus-data/master/tests-by-zcta.csv'
    download_document(url, location_source + ext)

    with open(location_source + ext,"r") as source:
        reader = csv.reader(source)
        with open(os.path.join(get_path(), location + ext),"w") as result:
            writer = csv.writer(result)
            writer.writerow(header)
            for row in reader:
                write_row(writer, url, row[0], row[1])
    os.remove(location_source + ext)

# fetch_nyc()
