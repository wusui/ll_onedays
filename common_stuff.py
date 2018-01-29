#!/usr/bin/python
"""
Common stuff used by all the other routines.  This is the lowest
level py file in that all other files use methods and variables
defined in this module.

Global varables and defaults:
    LLSAVE_LOCATION -- default directory or folder where files created
                       will be stored.
    HELLO_MY_NAME_IS -- default user name
    EXT_FILES -- list of file names that will be storede in LLSAVE_LOCATION

get_percentile function: Used to calculated a player's percentile rank.

doc_funtions: Give further explanation of things when the -x parameter is
              passed on the command line.
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
    """
    Compute the percentile for this position.

    Input:
        total -- total number of players in this quiz
        place -- place we took
        ties -- number of players that we are tied with

    Returns:
        percentile that we finished.  Integer value rounded down.
    """
    numer = total - place - ties + 1
    if numer < 0:
        numer = 0
    numer *= 100
    pctile = numer // total
    return pctile


def doc_indata():
    """
    LEARNED LEAGUE FILE FORMATS

    The names and formats of files containing information for each one-day
    have changed over time.  All of the examples below are files on
    http://www.learnedleague.com/.   XXX in each of these examples is a
    descriptive label for each quiz (audreyhepburn, arizona, skiing).

    From January 1, 2018 to the present, one-day informations has been stored
    in csv format in files named oneday/csv/xxx.csv

    From July 31, 2014 to January 1, 2018, all one-day pages had
    "All Player" tabs.   Information on these pages can be found in
    oneday/results.php?xxx&1.  Internally the format changed on
    October 1, 2015

    From February 28, 2012 to July 31, 2014, one-day page data can be found
    in files named oneday.php?xxx

    From January 1, 2012 to Feb 28, 2012 one-day page data can be found in
    files named: oneday/xxx.php

    Prior to January 1, 2012, one-day dadta can be found in
    oneday/xxx.shmtl

    All oneday files are listed in https://learnedleague.com/oneday/
    """
    print(doc_indata.__doc__)


def doc_outdata():
    """
    OUTPUT FILES

    Files are are written to either the default LLSAVE_LOCATION or to
    whatever directory was specified by --dir on the command line.

    The following six files are stored there:

    1. my_results.yml and our_results.yml -- Data extracted for a user or for
       everbody.  Used as a checkpoint file, data here is saved in the format
       described by -x formats.

    2. my_records.txt and our_records.txt -- Text describing the
       best and worst return per correctly answered question.  Contains
       associated quizzes, dates, and in the case of our_records.txt, users.

    3. my_table.html and our_table.html -- html formated table showing
       the best and worst returns per question.
    """
    print(doc_outdata.__doc__)


def doc_formats():
    """
    FORMAT OF OBJECTS PASSED BETWEEN FUNCTIONS

    1. One-days quizzes: A list, each entry of which represents an individual
       one day quiz.  Each quiz entry is a list containg three items:
        a. Partial name of the html of php file that data gets extracted from
        b. Name of the one-day quiz
        c. Date of the one-day quizzes.
       This data is returned by main_read in read_main_page.py

    2. Individual results: A dictionary indexed by quiz name.  Each entry
       is a dictionary containing the following values:
        a. Quiz name
        b. Quiz date
        c. Number that we got correct
        d. Where we finished
        e. Number of players we tied.
        f. Total number of players in this quiz
       This data is used by one_day in main.py and is stored in my_result.yml

    3. Results for all players: A dictionary containing an entry for each quiz.
       Each entry is indexed by the quiz name and is list of three items:
        a. The best return for each question
        b. The worst return for each question
        c. A list containing the url, name, and date of this quiz.
       Returns are dictionaries indexed by questions correct.  The data
       in each return dictionary entry is a list consisting of the best or
       worst percentile value for this number of questions, and a list of
       players who scored in that percentile.

    All dates are converted to datetime values and stored as strings using
    the "Mon DD, YYYY" format.
    """
    print(doc_formats.__doc__)

DOC_LINKS = {'in_data': doc_indata, 'out_data': doc_outdata,
             'formats': doc_formats}
