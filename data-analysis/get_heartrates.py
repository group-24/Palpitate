#!/usr/bin/python

from openpyxl import load_workbook
from xlrd import open_workbook as load_xls
import xlrd

import numpy as np
from interesting_moments import moments
import os

def get_heartrates(pathToHeartAV, window=4):
    """Returns a dicitionary of <subjectID>_<state> -> {[heartrates], start_time}, each entry in the
    heratrates array for that subject is the mean heartrate for that time window
    (default window: 4)"""

    workbook = load_workbook(pathToHeartAV + 'SensorData/HeartAV_HeartRateFiles/HeartRate.xlsx')

    heartrates = {}
    for page in workbook.get_sheet_names():
        worksheet = workbook[page]
        heartrate_column = worksheet.columns[1] # the B column contains the data we want
        heartrate_column = heartrate_column [1:] # trim the top level

        start_time_cell =  worksheet.columns[0][1]
        start_time_value = start_time_cell.value
        # print('value of time: ' + str(start_time_value)),

        # time formats differ between worksheets
        if isinstance(start_time_value, float):
            start_time = get_tuple_for_time_from_exel(start_time_cell, 0)
        else:
            start_time = (start_time_value.hour, start_time_value.minute, start_time_value.second)
        # print('value: ', start_time)

        number_seen = 0
        number_legal = 0
        sum_heartrate = 0
        data = []
        for heartrate in  heartrate_column:
            value = heartrate.value
            number_seen += 1

            if isinstance(value, (float, long, int)) and value != 0:
                number_legal += 1
                sum_heartrate += value

            if number_seen == window and number_legal != 0:
                mean_heartrate = sum_heartrate/number_legal
                data.append(mean_heartrate)
                number_seen = 0
                number_legal = 0
                sum_heartrate = 0

        # heartrates[get_subjectID_and_state(page)] = np.array(data)
        heartrates[get_subjectID_and_state(page)] = {
            'heartrates': np.array(data),
            'start': start_time
            }

    return heartrates

def get_subjectID_and_state(subjectID):
    index_to_trim_from = 3
    if subjectID[3] == '0':
        index_to_trim_from = 4

    return subjectID[index_to_trim_from:index_to_trim_from+5]


def get_interesting_heartrates(pathToHeartAV, window=4):
    """Returns a dicitionary of <subjectID>_<state> -> [{time, bpm, description}],
    where we only take moments from when a subject is talking
    (default window: 4)"""

    # SETUP: opening all of the files
    heartrate_timings = get_heartrates(pathToHeartAV, 1);

    time_info_workbooks = {}
    path_to_logs = pathToHeartAV + 'MetaData/HeartAV_HCITaskLogfiles'
    for workbook_name in os.listdir(path_to_logs):
        workbook = load_xls(path_to_logs + '/' + workbook_name)
        subject_label = workbook_name[1:6]
        time_info_workbooks[subject_label] = workbook
    # End SETUP

    heartrate_data = {}
    # go though each subject_state and get all of the intersting times
    for subject_state in time_info_workbooks.keys():
        # not all of the event logs are in the heartrate_timings
        if subject_state not in heartrate_timings:
            continue

        data_for_subject_state = []
        time_info_worksheet = time_info_workbooks[subject_state].sheet_by_index(0)

        for rowidx in range(2, time_info_worksheet.nrows):
            row = time_info_worksheet.row(rowidx)
            activity = row[1].value
            # check to see if it qualifies as a period where the subject speaks
            if activity in moments:
                print('getting data for: ' + activity + ' in ' + subject_state)
                start_time = get_tuple_for_time_from_exel(row[5], 0)
                # HACK: this really is
                end_time = get_end_time_for(time_info_worksheet, rowidx)
                # end_time = get_tuple_for_time_from_exel(time_info_worksheet.row(rowidx+1)[5], 0)

                data_for_subject_state.append(get_info_for(subject_state, start_time, end_time, activity, heartrate_timings))

        heartrate_data[subject_state] = np.array(data_for_subject_state)

    return heartrate_data

def get_end_time_for(worksheet, rowidx):
    i = 0
    while(True):
        i += 1
        if not (worksheet.cell_type(rowidx, 5) in (xlrd.XL_CELL_EMPTY, xlrd.XL_CELL_BLANK)):
            # print('found row at ' + str(i))
            return worksheet.row(rowidx + i)[5]


def get_info_for(subject_state, start_time, end_time, activity, heartrate_timings):
    """Returns a list containing all of the heartrate quanta for a particular moment"""
    # print('SUCESS!! start time:' + str(start_time))




# from: http://stackoverflow.com/questions/17140652/read-time-from-excel-sheet-using-xlrd-in-time-format-and-not-in-float
def get_tuple_for_time_from_exel(cell_with_excel_time, wb):
    """Returns a (hour, minute, second) of the time from the excel spreadsheet"""
    return xlrd.xldate_as_tuple(cell_with_excel_time.value, wb)[3:]
