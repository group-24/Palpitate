#!/usr/bin/python

# This script extracts the information from the heartAV database xlsx failure
# so that we can get hold of the heartRate for the 4 second periods more easlily

# note for me /Volumes/SAMSUNG/HeartAV/SensorData/HeartAV_HeartRateFiles/HeartRate.xlsx

# arguments for the program
# <subject id>
# <path to the xlsx file>
# <output path>

import sys
from openpyxl import load_workbook

if len(sys.argv) < 4:
    print "ERROR: please give a subject id and a destination path"
    sys.exit()

subject_id = sys.argv[1]
path_to_xlsx = sys.argv[2]
output_path = sys.argv[3]

wb2 = load_workbook(path_to_xlsx)
print wb2.get_sheet_names()
