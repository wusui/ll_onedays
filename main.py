#!/usr/bin/python
""" TO DO: """
import os
import operator
import yaml

from common_stuff import ALL_RECORDS
from common_stuff import SAVED_ONES
from common_stuff import LLCSV_LOCATION
from common_stuff import HELLO_MY_NAME_IS
from common_stuff import get_percentile
from make_table import make_table
from collect_data import collect_data

MY_RECS = os.sep.join([LLCSV_LOCATION, 'my_records.txt'])
OUR_RECS = os.sep.join([LLCSV_LOCATION, 'our_records.txt'])
OUTFILE = os.sep.join([LLCSV_LOCATION, 'my_table.html'])
ALLOUTFILE = os.sep.join([LLCSV_LOCATION, 'our_table.html'])

def display(header, data):
    """ TO DO: """
    resp = '\n\n\n            %s Finish\n\n' % header
    for quiz_rec in range(1, 13):
        fline = '%d correct: %d percentile\n' % (quiz_rec,
                                                 data[quiz_rec]['pctile'])
        resp = ''.join([resp, fline])
        if len(data[quiz_rec]['data']) > 10:
            resp = ''.join([resp, '    Lots\n'])
            continue
        for quiz in data[quiz_rec]['data']:
            sline = '    %s: %s' % (quiz['date'], quiz['name'])
            resp = ''.join([resp, sline])
            if 'people_total' in quiz.keys():
                resp = ''.join([resp, ' (%d)' % quiz['people_total']])
            resp = ''.join([resp, '\n'])
    resp = ''.join([resp, '\n\n'])
    return resp

def my_compute_inner(qdata, pctile, hlval, correct, comparer):
    """ TO DO: """
    if not correct in hlval.keys():
        hlval[correct] = {'pctile': pctile, 'data': [qdata]}
        return
    if pctile == hlval[correct]['pctile']:
        hlval[correct]['data'].append(qdata)
    if comparer(pctile, hlval[correct]['pctile']):
        hlval[correct] = {'pctile': pctile, 'data': [qdata]}

def my_compute(qdata, hival, loval):
    """ TO DO: """
    pctile = get_percentile(qdata['total'], qdata['place'], qdata['tiecount'])
    correct = qdata['correct']
    if correct == 0:
        return
    my_compute_inner(qdata, pctile, hival, correct, operator.gt)
    my_compute_inner(qdata, pctile, loval, correct, operator.lt)

def our_compute_inner(qdata, hlval, indx, comparer):
    """ TO DO: """
    for hlkey in qdata[0][indx].keys():
        dpart = {}
        dpart['correct'] = hlkey
        dpart['date'] = qdata[1][2]
        dpart['name'] = qdata[1][1]
        dpart['people_total'] = len(qdata[0][0][hlkey][1])
        lpercent = qdata[0][0][hlkey][0]
        if not hlkey in hlval.keys():
            hlval[hlkey] = {'pctile': lpercent}
            hlval[hlkey]['data'] = [dpart]
            continue
        if hlval[hlkey]['pctile'] == lpercent:
            hlval[hlkey]['data'].append(dpart)
        if comparer(hlval[hlkey]['pctile'], lpercent):
            hlval[hlkey] = {'pctile': lpercent}
            hlval[hlkey]['data'] = [dpart]

def our_compute(qdata, hival, loval):
    """ TO DO: """
    our_compute_inner(qdata, hival, 0, operator.lt)
    our_compute_inner(qdata, loval, 1, operator.gt)

def my_one_days(player):
    """ TO DO: """
    collect_data(player)
    lindex = 0
    if player == ' ':
        lindex = 1
    yaml_files = ALL_RECORDS if lindex else SAVED_ONES
    reports = OUR_RECS if lindex else MY_RECS
    data_hndlr = our_compute if lindex else my_compute
    outfile = ALLOUTFILE if lindex else OUTFILE
    with open(yaml_files, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        hival = {}
        loval = {}
        for quiz in data.keys():
            qdata = data[quiz]
            data_hndlr(qdata, hival, loval)
        tot_quiz = "Total quizzes played: %d" % len(data)
        outstr = ''.join([tot_quiz, display('Best', hival),
                          display('Worst', loval)])
        with open(reports, 'w') as filedesc:
            filedesc.write(outstr)
        make_table(hival, loval, outfile, False)

if __name__ == '__main__':
    my_one_days(HELLO_MY_NAME_IS)
    my_one_days(' ')
