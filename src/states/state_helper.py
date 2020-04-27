import re
from datetime import datetime

header = ["Zip Code", "Confirmed COVID-19 Cases", "Confirmed COVID-19 Deaths", "Date", "Source URL"]

def is_int(value):
    try:
        int(value)
        return True
    except:
        return False

def extract_cases(cases):
    if(cases == "" or is_int(cases)):
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