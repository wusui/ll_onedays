#!/usr/bin/python
"""
Figure out stats about one user's onedays.

Oneday information extracted after January 1, 2018 will appear in .csv
files in llcsvfiles.

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
LLCSV_ALL = {'Windows': os.sep.join(['C:', 'Users', 'Warren', 'llcsvfiles']),
             'Linux': os.sep.join(['/home', 'wusui', 'll_my_onedays',
                                   'llcsvfiles'])}
LLCSV_LOCATION = LLCSV_ALL[platform.system()]
HELLO_MY_NAME_IS = 'UsuiW'
SAVED_ONES = os.sep.join([LLCSV_LOCATION, 'result.yml'])
ALL_RECORDS = os.sep.join([LLCSV_LOCATION, 'allinfo.yml'])

def get_percentile(total, place, ties):
    """ TO DO: """
    numer = total - place - ties + 1
    if numer < 0:
        numer = 0
    numer *= 100
    pctile = numer // total
    return pctile
