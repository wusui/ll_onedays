#!/usr/bin/python
import os
import operator
from html.parser import HTMLParser
import requests
from CommonStuff import get_percentile
from CommonStuff import LLCSV_LOCATION

class ParseBestW(HTMLParser):
    def __init__(self, player):
        HTMLParser.__init__(self)
        self.hinumbs = {}
        self.lonumbs = {}
        self.posis = 0
        self.scanforPos = False
        self.scanforName = False
        self.scanforScores = False
        self.size = 0
        self.right = 0
        self.wrong = 0
        self.ties = {}

    def handle_starttag(self, tag, attrs):
        if not self.scanforPos:
            for apt in attrs:
                if apt[0] == 'class':
                    if apt[1] == 'std-midleft':
                        self.scanforPos = True
    def handle_data(self, data):
        def numbset(self, hlval, comparer):
            if not self.right in hlval:
                if self.right > 0:
                    hlval[self.right] = [self.posis, [self.person]]
            else:
                if comparer(hlval[self.right][0],self.posis):
                    hlval[self.right] = [self.posis, [self.person]]
                if hlval[self.right][0] == self.posis:
                    hlval[self.right][1].append(self.person)
        if self.scanforScores:
            try:
                nval = int(data)
            except ValueError:
                print('%s is invalid numerical input' % data)
                return
            if nval == 0:
                self.wrong += 1
            else:
                self.right += 1
            if (self.right + self.wrong) == 12:
                if not self.posis in self.ties.keys():
                    self.ties[self.posis] = 1
                else:
                    self.ties[self.posis] += 1
                #print('Right %d' % self.right)
                numbset(self, self.hinumbs, operator.lt)
                numbset(self, self.lonumbs, operator.gt)
                self.size += 1
                self.scanforScores = False
                self.right = 0
                self.wrong = 0
        if self.scanforName:
            if data[0].isalpha():
                self.person = data
            else:
                self.person = data[1:]
            self.scanforPos = False
            self.scanforName = False
            self.scanforScores = True
        if self.scanforPos:
            if data.endswith('.'):
                strval = data[0:-1]
                try:
                    self.posis = int(strval)
                except ValueError:
                    return
                #print("position: %d" % self.posis)
                self.scanforName = True

def FindBandW(filen, player):
    our_text = requests.get(filen)
    parser = ParseBestW(player)
    parser.feed(our_text.text)
    for coransval in parser.hinumbs.keys():
        place = parser.hinumbs[coransval][0]
        ties = parser.ties[place]
        lplace = parser.lonumbs[coransval][0]
        parser.hinumbs[coransval][0] = get_percentile(parser.size, place, ties)
        parser.lonumbs[coransval][0] = get_percentile(parser.size, lplace, ties)
    return [parser.hinumbs, parser.lonumbs]

def AllCsvIn(hlcsv, correct, pct, parts, comparer):
    if not correct in hlcsv.keys():
        hlcsv[correct] = [pct,[parts[1]]]
    else:
        if pct == hlcsv[correct][0]:
            hlcsv[correct][1].append(parts[1])
        if comparer(pct, hlcsv[correct][0]):
            hlcsv[correct] = [pct,[parts[1]]]

def AllCsv(filen, player):
    hicsv = {}
    locsv = {}
    with open(filen) as f:
        data = f.read()
        records = data.split('\n')
        total = len(records) - 2
        ties = {}
        for record in records[1:]:
            parts = record.split(',')
            if len(parts) < 2:
                continue
            indx = int(parts[2])
            if not indx in ties.keys():
                ties[indx] = 1
            else:
                ties[indx] += 1
        for record in records:
            correct = 0
            parts = record.split(',')
            if parts[0] == 'Season':
                continue
            if len(parts) < 2:
                continue
            for i in range(5,17):
                correct += int(parts[i])
            if correct == 0:
                continue
            place = int(parts[2])
            pct = get_percentile(total, place, ties[place])
            AllCsvIn(hicsv, correct, pct, parts, operator.gt)
            AllCsvIn(locsv, correct, pct, parts, operator.lt)
        return [hicsv, locsv]
    return False

if __name__ == '__main__':
    testlist = ['https://learnedleague.com/oneday/results.php?endings&1',
                'https://learnedleague.com/oneday/results.php?americanwildlife&1',
                'https://learnedleague.com/oneday.php?kentucky',
                'https://learnedleague.com/oneday.php?tennis',
                'https://learnedleague.com/oneday/skiing.php',
                'https://learnedLeague.com/oneday/paulmccartney.shmtl',
                'https://learnedleague.com/oneday/results.php?classic_72&1',
                'https://learnedleague.com/oneday.php?tourdefrance']
    for filev in testlist:
        result = FindBandW(filev, '')
        print(result)
    testlist = ['lifeonearth',
                'ogdennash',
                'algorithms',
                '90salternativemusic']
    for filev in testlist:
        fullpath = os.sep.join([LLCSV_LOCATION, filev])
        fullpath = ''.join([fullpath, '.csv'])
        result = AllCsv(fullpath, ' ')
        print(result)
