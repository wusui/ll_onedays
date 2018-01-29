#!/usr/bin/python
"""
Main routine

In addition to organizing the data collected, this file also contains the
command line parser and output string formatter for *_records.txt files.
"""
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
    """
    Generate the text of results found.  This will be returned and later saved
    in my_records.txt or our_records.txt

    Input:
        header -- Type of data ('best' return or 'worst' return)
        data -- dictionary of results collect in hival or loval dictionaries
                (see use of hival and loval in the routines below)

    Returns:
        Human readable string to be stored in txt files.
    """
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
    """
    Do the actual saving of best and worst return values for all users.

    Input:
        qdata -- List of quiz data
        pctile -- percentile we are in for this quiz
        hlval -- dictionary to be initialized with best or worst returns.
        indx -- 0 if best returns, 1 if worst returns.
        comparer -- operator.lt or operator.gt (depending on best or worst)

    Returns:
        hlval is updated.
    """
    if correct not in hlval.keys():
        hlval[correct] = {'pctile': pctile, 'data': [qdata]}
        return
    if pctile == hlval[correct]['pctile']:
        hlval[correct]['data'].append(qdata)
    if comparer(pctile, hlval[correct]['pctile']):
        hlval[correct] = {'pctile': pctile, 'data': [qdata]}


def my_compute(qdata, hival, loval):
    """
    Calculate a percentile value for the user's game specified.
    Call my_compute_inner separately with hival and loval.

    Input:
        qdata -- list of quiz data extracted from the information saved in
                 the appropriate yaml file.
        hival -- dictionary where the best return values found are kept.  This
                 structure will end up containing, for each number of questions
                 missed, a percentile value and a list of quiz records with
                 the best return.
        loval -- dictionary where the worst return values found are kept.  It
                 has the same format as hival.

    Returns:
        hival and loval are updated.
    """
    pctile = get_percentile(qdata['total'], qdata['place'], qdata['tiecount'])
    correct = qdata['correct']
    if correct == 0:
        return
    my_compute_inner(qdata, pctile, hival, correct, operator.gt)
    my_compute_inner(qdata, pctile, loval, correct, operator.lt)


def our_compute_inner(qdata, hlval, indx, comparer):
    """
    Do the actual saving of best and worst return values for all users.

    Input:
        qdata -- List of quiz data
        hlval -- dictionary to be initialized with best or worst returns.
        indx -- 0 if best returns, 1 if worst returns.
        comparer -- operator.lt or operator.gt (depending on best or worst)

    Returns:
        hlval is updated.
    """
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
    """
    Call our_compute_inner separately with hival and loval.

    Input:
        qdata -- list of quiz data extracted from the information saved in
                 the appropriate yaml file.
        hival -- dictionary where the best return values found are kept.  This
                 structure will end up containing, for each number of questions
                 missed, a percentile value and a list of quiz records with
                 the best return.
        loval -- dictionary where the worst return values found are kept.  It
                 has the same format as hival.

    Returns:
        hival and loval are updated.
    """
    our_compute_inner(qdata, hival, 0, operator.lt)
    our_compute_inner(qdata, loval, 1, operator.gt)


def one_days(player, params):
    """
    Main routine.

    First call collect_data to generate the appropriate yaml file, if needed.

    Then loop through all entries in the yaml file to find the quizzes with the
    best and worst returns. Write the appropriate text file.

    Finally call make_table to generate the appropriate html file.

    Input:
        player: Individual player name. Blank means all players.
        params: parsed command line parameters, and file names

    Output:
        no data returned.  Appropriate yml, txt, and html files are generated.
    """
    collect_data(player, params)
    yaml_files = params['our_result'] if player == ' ' else params['my_result']
    reports = params['our_records'] if player == ' ' else params['my_records']
    data_hndlr = our_compute if player == ' ' else my_compute
    outfile = params['our_table'] if player == ' ' else params['my_table']
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
    """
    Parse the command line.  Command line options are described by the
    -h or --help option.

    If neither 'me' or 'all' option is specified, both are set.
    Also add file names as keys into the parser Namespace, where each
    entry points to the physical full path where the file is located.

    Input:
        cmd_line: arguments passed to the main program (argv[0] missing)

    Returns: dictionary of parsed argument values, and entries of files
             to be generated.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--dir', nargs='?', const=LLSAVE_LOCATION,
                        default=LLSAVE_LOCATION,
                        help='Location of files produced')
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
    """
    Wrapper for parser and one_day calls.
    After doing command line parsing, handle the explanation calls separately
    from the one_day calls.  Perform one_day calls for individual user and/or
    for all users.  Output files end up getting stored in the directory
    specified by the dir option, or in LlSAVE_LOCATION in common_stuff by
    default.
    """
    largs = get_args(sys.argv[1:])
    if largs['explain']:
        try:
            DOC_LINKS[largs['explain'][0]]()
        except KeyError:
            print("Don't know much about %s" % largs['explain'][0])
        return
    if largs['me']:
        one_days(largs['user'], largs)
    if largs['all']:
        one_days(' ', largs)
    return

if __name__ == "__main__":
    main_rtn()
