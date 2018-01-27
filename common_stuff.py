#!/usr/bin/python
"""
Figure out stats about one user's onedays.

Oneday information extracted after January 1, 2018 will appear in .csv
files in llsvfiles.

Oneday information extracted between July 31, 2014 and January 1, 2018 have All
player tabs.  To extract information, use:
https://learnedleague.com/oneday/results.php?sportsgeography&1
Internally format changed October 1, 2015

Oneday information extracted between February 28, 2012 and *July 31, 2014*
is contained in files named: https://learnedleague.com/oneday.php?arizona

Oneday information from January 1, 2012 to Feb 28, 2012 is contained
in files named: https://learnedleague.com/oneday/skiing.php

Oneday information prior to January 1, 2012 is containe infiles named:
http://learnedleague.com/oneday/paulmccartney.shmtl

All oneday files are listed in https://learnedleague.com/oneday/

TODO: Clean up this document and put in function. print(docf.__doc__)
"""
import os
import platform
LLSAVE_ALL = {'Windows': os.sep.join(['C:', 'Users', 'Warren', 'llsvfiles']),
             'Linux': os.sep.join(['/home', 'wusui', 'll_my_onedays',
                                   'llsvfiles'])}
LLSAVE_LOCATION = LLSAVE_ALL[platform.system()]
HELLO_MY_NAME_IS = 'UsuiW'
EXT_FILES = ['my_records.txt', 'our_records.txt',
             'my_table.html', 'our_table.html',
             'my_result.yml', 'our_result.yml']


def get_percentile(total, place, ties):
    """ TO DO: """
    numer = total - place - ties + 1
    if numer < 0:
        numer = 0
    numer *= 100
    pctile = numer // total
    return pctile


def doc_indata():
    """ TO DO: """
    print(doc_indata.__doc__)


def doc_outdata():
    """ TO DO: """
    print(doc_outdata.__doc__)


def doc_formats():
    """ TO DO: formats """
    print(doc_formats.__doc__)

DOC_LINKS = {'in_data': doc_indata, 'out_data': doc_outdata,
             'formats': doc_formats}
