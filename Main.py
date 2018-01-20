#!/usr/bin/python
import os
import yaml
import operator
from CommonStuff import ALL_RECORDS
from CommonStuff import SAVED_ONES
from CommonStuff import LLCSV_LOCATION
from CommonStuff import get_percentile
from MakeTable import MakeTable
from CollectData import CollectData

MY_RECS = os.sep.join([LLCSV_LOCATION, 'my_records.txt'])
OUR_RECS = os.sep.join([LLCSV_LOCATION, 'our_records.txt'])
OUTFILE = os.sep.join([LLCSV_LOCATION, 'my_table.html'])
ALLOUTFILE = os.sep.join([LLCSV_LOCATION, 'our_table.html'])

def Display(header, data):
    resp = '\n\n\n            %s Finish\n\n' % header
    for qr in range(1,13):
        fline = '%d correct: %d percentile\n' % (qr, data[qr]['pctile'])
        resp = ''.join([resp, fline])
        if len(data[qr]['data']) > 10:
            resp = ''.join([resp, '    Lots\n'])
            continue
        for quiz in data[qr]['data']:
            sline = '    %s: %s' % (quiz['date'], quiz['name'])
            resp = ''.join([resp, sline])
            if 'people_total' in quiz.keys():
                resp = ''.join([resp, ' (%d)' % quiz['people_total']])
            resp = ''.join([resp,'\n'])
    resp = ''.join([resp, '\n\n'])
    return resp

def my_compute_inner(qdata, pctile, hlval, correct, comparer):
    if not correct in hlval.keys():
        hlval[correct] = {'pctile': pctile, 'data': [qdata]}
        return
    if pctile == hlval[correct]['pctile']:
        hlval[correct]['data'].append(qdata)
    if comparer(pctile, hlval[correct]['pctile']):
        hlval[correct] = {'pctile': pctile, 'data': [qdata]}

def my_compute(qdata, hival, loval):
    pctile = get_percentile(qdata['total'], qdata['place'], qdata['tiecount'])
    correct = qdata['correct']        
    if correct == 0:
        return
    my_compute_inner(qdata, pctile, hival, correct, operator.gt)
    my_compute_inner(qdata, pctile, loval, correct, operator.lt)

def our_compute_inner(qdata, hlval, indx, comparer):
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
    our_compute_inner(qdata, hival, 0, operator.lt)
    our_compute_inner(qdata, loval, 1, operator.gt)
    
def MyOnedays(player):
    CollectData(player)
    lindex = 0
    if player == ' ':
        lindex = 1
    yaml_files = [SAVED_ONES, ALL_RECORDS][lindex]
    reports = [MY_RECS, OUR_RECS][lindex]
    data_hndlr = [my_compute, our_compute][lindex]
    outfile = [OUTFILE, ALLOUTFILE][lindex]
    with open(yaml_files, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        hival = {}
        loval = {}
        for quiz in data.keys():
            qdata = data[quiz]
            data_hndlr(qdata, hival, loval)
        tq = "Total quizzes played: %d" % len(data)
        outstr = ''.join([tq, Display('Best', hival),Display('Worst', loval)])
        with open(reports, 'w') as f:
            f.write(outstr)
        MakeTable(hival, loval, outfile, False)

if __name__ == '__main__':
    from CommonStuff import HELLO_MY_NAME_IS
    MyOnedays(HELLO_MY_NAME_IS)
    MyOnedays(' ')
