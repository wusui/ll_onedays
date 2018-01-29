#!/usr/bin/python
"""
Extract the day from html pages.  This code mostly keeps track
of both single users and all users, and calls the appropriate
data extraction routines based on the type of user and the date
of each quiz.
"""
import os.path
from datetime import datetime
import yaml
from read_main_page import main_read
from analyze_this import analyze_this
from all_things import find_best_n_worst
from all_things import all_csv
from extract_csv import extract_csv


DATE_FMT = '%b %d, %Y'
SWITCH_DATE = datetime.strptime('Jul 14, 2014', DATE_FMT)
USE_CSV_DATE = datetime.strptime('Jan 1, 2018', DATE_FMT)
LFORMAT = 'https://learnedleague.com/oneday/results.php?%s&1'
OFORMAT = 'http://www.learnedleague.com/oneday/csv'


def all_merge(result, retval, quiz):
    """
    Merge data for a quiz for all users

    Input:
        result -- quiz data parsed
        retval -- list to be updated
        quiz -- individual quiz data

    Returns:
        retval is updated  with the result and quiz information.
    """
    retval[quiz[1]] = [result, quiz]
    print(retval[quiz[1]])


def handle_collection(result, retval, quiz):
    """
    Merge data for a quiz for an individual user

    Input:
        result -- quiz data parsed
        retval -- list to be updated
        quiz -- individual quiz data

    Returns:
        retval is updated  with the result and quiz information.
    """
    if not result:
        print("You did not play %s" % quiz[1])
    else:
        retval[quiz[1]] = {}
        retval[quiz[1]]['name'] = quiz[1]
        retval[quiz[1]]['date'] = quiz[2]
        retval[quiz[1]]['correct'] = result[0][2]
        retval[quiz[1]]['place'] = result[0][0]
        retval[quiz[1]]['total'] = result[1]
        retval[quiz[1]]['tiecount'] = result[2]
        print(retval[quiz[1]])


def do_collection(name, anal_func, setdata_func, csv_func):
    """
    Input:
        name -- user name or blank for all users.
        anal_func -- analysis function (see analyze_this for individual
                     users, and all_things for all users
        setdata_function -- local handle_collection for individual users
                            or all_merge for all users
        csv_func -- csv reading/parsing function for either individual users
                    or all users.
    """
    retval = {}
    quizzes = main_read()
    for quiz in quizzes:
        if quiz[1].find('One-Day') >= 0:
            continue
        if quiz[1].find('Midseason') >= 0:
            continue
        qdate = datetime.strptime(quiz[2], DATE_FMT)
        if qdate > USE_CSV_DATE:
            csvfile = quiz[0].split('?')[-1]
            fullpath = '/'.join([OFORMAT, csvfile])
            fullpath = ''.join([fullpath, '.csv'])
            result = csv_func(fullpath, name)
        else:
            hfile = quiz[0]
            if qdate > SWITCH_DATE:
                parts = hfile.split('?')
                hfile = LFORMAT % parts[-1]
            if hfile.startswith("/oneday"):
                hfile = "http://learnedleague.com%s" % hfile
            result = anal_func(hfile, name)
        setdata_func(result, retval, quiz)
    return retval


def collect_data(name, param):
    """
    Collect data, switching routines based on whether or not individual
    players or all players data is being collected.

    Input:
        name -- user's name (or blank if all users wanted)
        param -- parameters extracted from the command line

    Returns:
        No return value, but the appropriate yaml file is written
        (my_result.yaml or our_result.yaml)
    """
    progrm = 0
    if name == ' ':
        progrm = 1
    packgs = [[analyze_this, handle_collection, extract_csv,
               param['my_result']],
              [find_best_n_worst, all_merge, all_csv, param['our_result']]]
    parms = packgs[progrm]
    if os.path.isfile(parms[3]):
        print('%s already exists' % parms[3])
        return
    info = do_collection(name, parms[0], parms[1], parms[2])
    with open(parms[3], 'w') as yaml_file:
        yaml.dump(info, yaml_file, default_flow_style=False)
