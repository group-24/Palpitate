#!/usr/bin/python

# This script extracts the information from the heartAV database xlsx failure
# so that we can get hold of the heartRate for the 4 second periods more easlily

# note for me /Volumes/SAMSUNG/HeartAV/SensorData/HeartAV_HeartRateFiles/HeartRate.xlsx

# arguments for the program
# <path to the xlsx file>
# <output path>

import sys
from openpyxl import load_workbook

if len(sys.argv) < 3:
    print "ERROR: please give a subject id and a destination path"
    sys.exit()

path_to_xlsx = sys.argv[1]
output_path = sys.argv[2]

workbook = load_workbook(path_to_xlsx)
# page names = wb2.get_sheet_names()


for page in workbook.get_sheet_names():
    worksheet = workbook[page]
    heartrate_column = worksheet.columns[1] # the B column contains the data we want
    heartrate_column = heartrate_column [1:] # trim the top level

    number_seen = 0
    number_legal = 0
    sum_heartrate = 0
    file_data = ''
    for heartrate in  heartrate_column:
        value = heartrate.value
        number_seen += 1

        if isinstance(value, (float, long, int)) and value != 0:
            number_legal += 1
            sum_heartrate += value

        if number_seen == 4 and number_legal != 0:
            # print page + ": " + str(heartrate)

            mean_heartrate = sum_heartrate/number_legal
            file_data += str(mean_heartrate) + '\n'
            number_seen = 0
            number_legal = 0
            sum_heartrate = 0

    heartrate_file = open(page + '.txt', 'w')
    heartrate_file.write(file_data)
    heartrate_file.close()
