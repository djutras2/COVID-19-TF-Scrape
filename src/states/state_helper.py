header = ["Zip Code", "Confirmed COVID-19 Cases", "Confirmed COVID-19 Deaths", "Date", "Source URL"]

def is_int(value):
    try:
        int(value)
        return True
    except:
        return False

global path
path = ''

def get_path():
    global path
    return path

def set_path(p):
    print("Setting path to: " + p)
    global path
    path = p