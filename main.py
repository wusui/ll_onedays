#!/usr/bin/python
""" TO DO: """
import os
import sys
import operator
import argparse
import yaml

from common_stuff import LLSAVE_LOCATION
from common_stuff import HELLO_MY_NAME_IS
from common_stuff import EXT_FILES
from common_stuff import DOC_LINKS
from common_stuff import get_percentile
from make_table import make_table
from collect_data import collect_data


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
    if correct not in hlval.keys():
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
    if not qdata[0]:
        return
    for hlkey in qdata[0][indx].keys():
        dpart = {}
        dpart['correct'] = hlkey
        dpart['date'] = qdata[1][2]
        dpart['name'] = qdata[1][1]
        dpart['people_total'] = len(qdata[0][0][hlkey][1])
        lpercent = qdata[0][0][hlkey][0]
        if hlkey not in hlval.keys():
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


def my_one_days(player, params):
    """ TO DO: """
    collect_data(player, params)
    lindex = 0
    if player == ' ':
        lindex = 1
    yaml_files = params['our_result'] if lindex else params['my_result']
    reports = params['our_records'] if lindex else params['my_records']
    data_hndlr = our_compute if lindex else my_compute
    outfile = params['our_table'] if lindex else params['my_table']
    with open(yaml_files, 'r') as yaml_file:
        data = yaml.safe_load(yaml_file)
        vals = [{}, {}]
        for quiz in data.keys():
            qdata = data[quiz]
            if not qdata:
                continue
            data_hndlr(qdata, vals[0], vals[1])
        tot_quiz = "Total quizzes played: %d" % len(data)
        outstr = ''.join([tot_quiz, display('Best', vals[0]),
                          display('Worst', vals[1])])
        with open(reports, 'w') as filedesc:
            filedesc.write(outstr)
        make_table(vals[0], vals[1], outfile, params['bracket'])


def get_args(cmd_line):
    """ TO DO: """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', nargs='?', const=LLSAVE_LOCATION,
                        default=LLSAVE_LOCATION,
                        help='Location of .csv and files produced')
    parser.add_argument('-u', '--user', nargs='?', const=HELLO_MY_NAME_IS,
                        default=HELLO_MY_NAME_IS,
                        help='individual learned league user')
    parser.add_argument('-m', '--me', action='store_true',
                        help='Do analysis for individual user')
    parser.add_argument('-a', '--all', action='store_true',
                        help='Do analysis for all users')
    parser.add_argument('-b', '--bracket', action='store_true',
                        help='set square brackets in files produced')
    parser.add_argument('-x', '--explain', nargs=1,
                        help="in_data|out_data|formats")
    info = parser.parse_args(cmd_line)
    if not info.me and not info.all:
        info.me = True
        info.all = True
    for filev in EXT_FILES:
        fname = filev.split('.')
        sname = "--%s" % fname[0]
        parser.add_argument(sname)
        parser.parse_args([sname, os.sep.join([info.dir, filev])],
                          namespace=info)
    return vars(info)


def main_rtn():
    """ TO DO: """
    largs = get_args(sys.argv[1:])
    if largs['explain']:
        try:
            DOC_LINKS[largs['explain'][0]]()
        except KeyError:
            print("Don't know much about %s" % largs['explain'][0])
        return
    if largs['me']:
        my_one_days(largs['user'], largs)
    if largs['all']:
        my_one_days(' ', largs)
    return

if __name__ == "__main__":
    main_rtn()
