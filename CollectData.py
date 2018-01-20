#!/usr/bin/python
import os.path
import yaml
from datetime import datetime
from ReadMainPage import MainRead
from AnalyzeThis import AnalyzeThis
from AllThings import FindBandW
from AllThings import AllCsv
from ExtractCsv import ExtractCsv
from CommonStuff import SAVED_ONES
from CommonStuff import ALL_RECORDS
from CommonStuff import LLCSV_LOCATION

DATE_FMT = '%b %d, %Y'

class DataHandler(object):
    def __init__(self):
        self.switchDate = datetime.strptime('Jul 14, 2014', DATE_FMT)
        self.useCsvDate = datetime.strptime('Jan 1, 2018', DATE_FMT)
        self.fmt = 'https://learnedleague.com/oneday/results.php?%s&1'

def all_merge(result, retval, quiz):
    retval[quiz[1]] = [result, quiz]
    print(retval[quiz[1]])

def handle_collection(result, retval, quiz):
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

def doCollection(name, anal_func, setdata_func, csv_func):
    retval = {}
    dates = DataHandler()
    quizzes = MainRead()
    for quiz in quizzes:
        if quiz[1].find('One-Day') >= 0:
            continue
        if quiz[1].find('Midseason') >= 0:
            continue
        qdate = datetime.strptime(quiz[2], DATE_FMT)
        if qdate > dates.useCsvDate:
            csvfile = quiz[0].split('?')[-1]
            fullpath = os.sep.join([LLCSV_LOCATION, csvfile])
            fullpath = ''.join([fullpath, '.csv'])
            result = csv_func(fullpath, name)
        else:
            hfile = quiz[0]
            if qdate > dates.switchDate:
                parts = hfile.split('?')
                hfile = dates.fmt % parts[-1]
            if hfile.startswith("/oneday"):
                hfile = "http://learnedleague.com%s" % hfile
            result = anal_func(hfile, name)
        setdata_func(result, retval, quiz)
    return retval

def CollectData(name):
    progrm = 0
    if name == ' ':
        progrm = 1
    packgs = [[AnalyzeThis, handle_collection, ExtractCsv, SAVED_ONES],
              [FindBandW, all_merge, AllCsv, ALL_RECORDS]]
    parms = packgs[progrm]
    if os.path.isfile(parms[3]):
        print('%s already exists' % parms[3])
        return
    info = doCollection(name, parms[0], parms[1], parms[2])
    with open(parms[3], 'w') as yaml_file:
        yaml.dump(info, yaml_file, default_flow_style=False)

if __name__ == '__main__':
    from CommonStuff import HELLO_MY_NAME_IS
    CollectData(HELLO_MY_NAME_IS)
