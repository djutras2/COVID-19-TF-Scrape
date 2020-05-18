import re
from datetime import datetime
import os
from arcgis.gis import GIS
from arcgis.features import FeatureLayer

import csv

header = ["Zip Code", "Confirmed COVID-19 Cases", "Confirmed COVID-19 Deaths", "Date", "Source URL"]

def is_int(value):
    try:
        int(value)
        return True
    except:
        return False

def is_float(value):
    try:
        float(value)
        return True
    except:
        return False

def extract_cases(cases):
    if(cases == None):
        return ""

    if(cases == ""):
        return cases

    if(is_float(cases)):
        cases = int(float(cases))

    if(is_int(cases)):
        if(int(cases < 0)):
            return ""
        else:
            return cases

    # if("suppress" in cases.lower()):
    #     return ""

    for number in re.findall('[0-9]*', cases):
        if(number != ""):
            return number

    return ""

def create_row(source, zipcode, cases, deaths, date):
    if(date == None):
        date = datetime.date(datetime.now())

    return [zipcode.strip(), extract_cases(cases), extract_cases(deaths), date, source.strip()]
    
def write_row(writer, source, zipcode, cases = "", deaths = "", date = None):
    if(is_int(zipcode)):
        writer.writerow(create_row(source, zipcode, cases, deaths, date))

global path
path = ''

def get_path():
    global path
    return path

def set_path(p):
    print("Setting path to: " + p)
    global path
    path = p

def fetch_from_esri(file_name, url, zip_field, cases_field, deaths_field = ""):
    layer = FeatureLayer(url)

    # print(layer.properties.fields)

    fields = zip_field + "," + cases_field
    if(deaths_field != ""):
        fields += "," + deaths_field

    query = layer.query(out_fields=fields)
    
    with open(os.path.join(get_path(), file_name), 'w', encoding='utf-8') as out:
        writer = csv.writer(out)
        writer.writerow(header)

        for feature in query.features:
            if(deaths_field != ""):
                write_row(writer, url, feature.get_value(zip_field), feature.get_value(cases_field), feature.get_value(deaths_field))
            else:
                write_row(writer, url, feature.get_value(zip_field), feature.get_value(cases_field))