

header = ["Zip Code", "Confirmed COVID-19 Cases", "Confirmed COVID-19 Deaths", "Date", "Source URL"]

def is_int(value):
    try:
        int(value)
        return True
    except:
        return False