import os
import sys
import csv
import time

from datetime import datetime
from urllib.request import urlopen

test = False

directory = ""

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

    if not test:
        download_document(usafact_cases_data_url, usafact_cases_filename_temp)

    with open(usafact_cases_filename_temp, "r") as source:
        reader = csv.reader(source)
        header = next(reader)
        print(header)
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
                    schema.write("Col%d=%s Long\n" % (i+1, header[i].replace(" ", "_")))  
                else:
                    schema.write("Col%d=%s Long\n" % (i+1, header[i])) # .replace("/", "_").replace("'", "_")

        with open(os.path.join(directory, usafact_cases_filename), "w") as result:
            writer = csv.writer(result)
            writer.writerow(header)
            for row in reader:
                # TODO: insert real days of improvement algorithm
                days = 0
                for i in range(len(row) -1, 5, -1):
                    if(int(row[i]) < int(row[i-1])):
                        days += 1
                    else:
                        break

                row.append(str(days))

                # row[0] = "'" + row[0] + "'"

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