import os
import sys
import csv
import time

from datetime import datetime
from urllib.request import urlopen

test = False

directory = ""

def get_pop(pop_data, fips):
    for row in pop_data:
        if fips == row[0]:
            return float(row[3])
    return None

def download_document(document_url, file_name):
    response = urlopen(document_url)
    file = open(file_name, 'wb')
    file.write(response.read())
    file.close()

def main():
    print("fetching")

    days_of_improvement_header = "TEMP_Days of Improvement"
    usafact_cases_data_url = "https://usafactsstatic.blob.core.windows.net/public/data/covid-19/covid_confirmed_usafacts.csv"
    usafact_cases_filename = "usafact_cases.csv"
    usafact_cases_filename_temp = "usafact_cases_temp.csv"
    usafact_pop_data_filename = "recovery/covid_county_population_usafacts.csv"

    if not test:
        download_document(usafact_cases_data_url, usafact_cases_filename_temp)

    with open(usafact_cases_filename_temp, "r") as source:
        reader = csv.reader(source)
        header = next(reader)
        # print(header)
        for i in range(len(header)):
            if('/' in header[i]):
                header[i] = "'" + header[i] + "'"

        header.append(days_of_improvement_header)

        with open(os.path.join(directory, "schema.ini"), "w") as schema:
            schema.write("[%s]" % (usafact_cases_filename))
            schema.write('''
Format=CSVDelimited
ColNameHeader=True
Col1=countyFIPS Text Width 8000
Col2=County_Name Text Width 8000
Col3=State Text Width 8000
Col4=stateFIPS Long
''')

            for i in range(4, len(header)):
                if i == len(header) - 1:
                    schema.write("Col%d=%s Text Width 8000\n" % (i+1, header[i].replace(" ", "_")))  
                else:
                    schema.write("Col%d=%s Long\n" % (i+1, header[i])) # .replace("/", "_").replace("'", "_")

        with open(os.path.join(directory, usafact_cases_filename), "w") as result, open(usafact_pop_data_filename, "r") as pop:
            pop_data = csv.reader(pop)

            writer = csv.writer(result)
            writer.writerow(header)
            for row in reader:

                moving_average = []

                for i in range(len(row) - 15, len(row) - 1):
                    moving_average.append((float(row[i]) + float(row[i-1]) + float(row[i-2])) / 3.0)

                two_week_incidence = moving_average[13] - moving_average[0] # sum(moving_average)
                slope = two_week_incidence / 14.0

                # 6 Categories:
                # print(moving_average)

                # 5) no cases
                if(sum(moving_average) > 0):
                    # 1) sustained decline: if downward slope over 3 day-moving-averages over two weeks
                    # 4) 0-5 cases in past 2 weeks are considered to meet 14 day downward traj goal.
                    if(slope <= -.1 or two_week_incidence < 5.0):
                        days = "significant improvement"
                    else:
                        # 2) two-week low incidence <= 10 per 100,000
                        pop = get_pop(pop_data, row[0])
                        # print(pop)
                        # print(10 * pop / 100000.0)
                        # print(two_week_incidence)
                        if(two_week_incidence <= 10.0 * pop / 100000.0):
                            days = "low incidence some improvement"
                        # 3) two-week high incidence >= 10 per 100,000 and slope -.1 <= x <= .1 for no more than 5 days
                        elif(two_week_incidence >= pop / 100,000  and slope >= -.1 and slope <= .1):
                            days = "high incidence some improvement"
                        # 6) no improvement
                        else:
                            days = "no improvement"
                else:
                    days = "no cases"

                row.append(str(days))
                writer.writerow(row)
    
    if not test:
        os.remove(usafact_cases_filename_temp)

if __name__ == "__main__":
    if(len(sys.argv) > 1) and os.path.exists(sys.argv[1]):
            directory = sys.argv[1]
    else:
        print("Invalid path.")
        directory = ".\\output"

    main()