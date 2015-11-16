#!/usr/bin/python

from openpyxl import load_workbook
from xlrd import open_workbook as load_xls
import xlrd

import numpy as np
from interesting_moments import moments
import os
import pickle

XLS_CACHE = 'xlsCache'
def check_cache(cache_file):
	with open(cache_file,'rb') as f:
		data = pickle.load(f)
		return data
def write_cache(cache_file, data):
	with open(cache_file,'wb') as f:
		pickle.dump(data, f)


def get_heartrates(pathToHeartAV, window=4):
    """Returns a dicitionary of <subjectID>_<state> -> {[heartrates], start_time}, each entry in the
    heratrates array for that subject is the mean heartrate for that time window
    (default window: 4)"""

    workbook = load_workbook(os.path.join(pathToHeartAV, 'SensorData', 'HeartAV_HeartRateFiles', 'HeartRate.xlsx'))

    heartrate_info = {}
    for page in workbook.get_sheet_names():
        worksheet = workbook[page]
        heartrate_column = worksheet.columns[1] # the B column contains the data we want
        heartrate_column = heartrate_column [1:] # trim the top level

        start_time_cell =  worksheet.columns[0][1]
        start_time_value = start_time_cell.value

        # time formats differ between worksheets
        if isinstance(start_time_value, float):
            start_time = get_tuple_for_time_from_exel(start_time_cell, 0)
        elif isinstance(start_time_value, str):
            start_time = (start_time_value[0:2], start_time_value[2:5], start_time_value[5:8])
        else:
            start_time = (start_time_value.hour, start_time_value.minute, start_time_value.second)

        number_seen = 0
        number_legal = 0
        sum_heartrate = 0
        data = []
        for heartrate in  heartrate_column:
            value = heartrate.value
            number_seen += 1

            if isinstance(value, (float, int, int)) and value != 0:
                number_legal += 1
                sum_heartrate += value

            if number_seen == window:
                if number_legal != 0:
                    mean_heartrate = sum_heartrate/number_legal
                    data.append(mean_heartrate)
                number_seen = 0
                number_legal = 0
                sum_heartrate = 0

        heartrate_info[get_subjectID_and_state(page)] = {
            'heartrates': np.array(data), #naming here is weird
            'start': start_time
            }

    return heartrate_info

def get_subjectID_and_state(subjectID):
    index_to_trim_from = 3
    if subjectID[3] == '0':
        index_to_trim_from = 4

    return subjectID[index_to_trim_from:index_to_trim_from+5]

def get_interesting_heartrates(pathToHeartAV, window=4):
    """Returns a dicitionary of <subjectID>_<state> -> [[description, time, bpm]],
    where we only take moments from when a subject is talking
    (default window: 4)"""
    try:
        return check_cache(XLS_CACHE)
    except FileNotFoundError:
        pass

    # SETUP: opening all of the files
    heartrate_timings = get_heartrates(pathToHeartAV, 1);

    time_info_workbooks = {}
    path_to_logs = os.path.join(pathToHeartAV,'MetaData','HeartAV_HCITaskLogfiles')
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

        # data starts 2 rows down
        for rowidx in range(2, time_info_worksheet.nrows):
            row = time_info_worksheet.row(rowidx)
            activity = row[1].value
            # check to see if it qualifies as a period where the subject speaks
            if activity in moments:
                start_time = get_tuple_for_time_from_exel(row[5], 0)
                end_time = get_tuple_for_time_from_exel(get_end_time_for(time_info_worksheet, rowidx), 0)
                data_for_subject_state += get_info_for(subject_state, start_time, end_time, activity, heartrate_timings, window)

        heartrate_data[subject_state] = np.array(data_for_subject_state)

    write_cache(XLS_CACHE, heartrate_data)
    return heartrate_data

def get_end_time_for(worksheet, rowidx):
    """gets the end time of the activity at rowidx of the worksheet"""
    i = 0
    while True :
        i += 1
        if worksheet.cell_type(rowidx + i, 5) == xlrd.XL_CELL_DATE:
            return worksheet.row(rowidx + i)[5]


def get_info_for(subject_state, start_time, end_time, activity, heartrate_timings, window):
    """Returns a list containing all of the heartrate quanta for a particular activity"""
    info_for_session = heartrate_timings[subject_state]
    start_time_for_session = info_for_session['start']
    heartrates = info_for_session['heartrates']

    seconds_after = seconds_differece(start_time_for_session, start_time)
    period_of_moment = seconds_differece(start_time, end_time)

    total_heartrate = 0
    data = []
    number_in_batch = 0
    for i in range(period_of_moment):
        if seconds_after + i >= len(heartrates):
            break
        number_in_batch += 1
        total_heartrate += heartrates[seconds_after + i]
        if number_in_batch == window:
            mean_heartrate = total_heartrate / window
            # HACK: this represents: activity, start_time, heartrate
            data.append([activity, seconds_after + i - window, mean_heartrate])
            number_in_batch = 0
            total_heartrate = 0

    return data


# from: http://stackoverflow.com/questions/17140652/read-time-from-excel-sheet-using-xlrd-in-time-format-and-not-in-float
def get_tuple_for_time_from_exel(cell_with_excel_time, wb):
    """Returns a (hour, minute, second) of the time from the excel spreadsheet"""
    return xlrd.xldate_as_tuple(cell_with_excel_time.value, wb)[3:]


def seconds_differece(start, end):
    hours_diff = end[0] - start[0]
    minutes_diff = end[1] - start[1]
    seconds_diff = end[2] - start[2]
    return seconds_diff + (60 * minutes_diff) + (3600 * hours_diff)
