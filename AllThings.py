#!/usr/bin/python
"""
TO DO: fill me in.
"""
import operator
from html.parser import HTMLParser
import requests
from CommonStuff import get_percentile

class ParseBestW(HTMLParser):
    """
    TO DO: fill me in
    """
    def __init__(self):
        HTMLParser.__init__(self)
        self.person = ''
        self.hinumbs = {}
        self.lonumbs = {}
        self.intv = {}
        self.intv['posis'] = 0
        self.scan_for = {}
        self.scan_for['pos'] = False
        self.scan_for['name'] = False
        self.scan_for['scores'] = False
        self.intv['size'] = 0
        self.intv['right'] = 0
        self.intv['wrong'] = 0
        self.ties = {}

    def handle_starttag(self, tag, attrs):
        """ TO DO: """
        if tag in []:
            return
        if not self.scan_for['pos']:
            for apt in attrs:
                if apt[0] == 'class':
                    if apt[1] == 'std-midleft':
                        self.scan_for['pos'] = True
    def handle_data(self, data):
        """ TO DO: """
        def numbset(self, hlval, comparer):
            """ TO DO: """
            if not self.intv['right'] in hlval:
                if self.intv['right'] > 0:
                    hlval[self.intv['right']] = [self.intv['posis'], [self.person]]
            else:
                if comparer(hlval[self.intv['right']][0], self.intv['posis']):
                    hlval[self.intv['right']] = [self.intv['posis'], [self.person]]
                if hlval[self.intv['right']][0] == self.intv['posis']:
                    hlval[self.intv['right']][1].append(self.person)
        def scan_set(self, data):
            """ TO DO: """
            if self.scan_for['name']:
                if data[0].isalpha():
                    self.person = data
                else:
                    self.person = data[1:]
                self.scan_for['pos'] = False
                self.scan_for['name'] = False
                self.scan_for['scores'] = True
            if self.scan_for['pos']:
                if data.endswith('.'):
                    strval = data[0:-1]
                    try:
                        self.intv['posis'] = int(strval)
                    except ValueError:
                        return
                    self.scan_for['name'] = True
        if self.scan_for['scores']:
            try:
                nval = int(data)
            except ValueError:
                print('%s is invalid numerical input' % data)
                return
            if nval == 0:
                self.intv['wrong'] += 1
            else:
                self.intv['right'] += 1
            if (self.intv['right'] + self.intv['wrong']) == 12:
                if self.intv['posis'] not in self.ties.keys():
                    self.ties[self.intv['posis']] = 1
                else:
                    self.ties[self.intv['posis']] += 1
                numbset(self, self.hinumbs, operator.lt)
                numbset(self, self.lonumbs, operator.gt)
                self.intv['size'] += 1
                self.scan_for['scores'] = False
                self.intv['right'] = 0
                self.intv['wrong'] = 0
        scan_set(self, data)

def find_best_n_worst(filen, player):
    """ TO DO: """
    if player != ' ':
        return False
    our_text = requests.get(filen)
    parser = ParseBestW()
    parser.feed(our_text.text)
    for coransval in parser.hinumbs:
        place = parser.hinumbs[coransval][0]
        ties = parser.ties[place]
        lplace = parser.lonumbs[coransval][0]
        parser.hinumbs[coransval][0] = get_percentile(parser.intv['size'], place, ties)
        parser.lonumbs[coransval][0] = get_percentile(parser.intv['size'], lplace, ties)
    return [parser.hinumbs, parser.lonumbs]

def all_csv_in(hlcsv, correct, pct, parts, comparer):
    """ TO DO: """
    if not correct in hlcsv.keys():
        hlcsv[correct] = [pct, [parts[1]]]
    else:
        if pct == hlcsv[correct][0]:
            hlcsv[correct][1].append(parts[1])
        if comparer(pct, hlcsv[correct][0]):
            hlcsv[correct] = [pct, [parts[1]]]

def all_csv(filen, player):
    """ TO DO: """
    if player != ' ':
        return False
    hicsv = {}
    locsv = {}
    with open(filen) as fileobj:
        records = fileobj.read().split('\n')
        total = len(records) - 2
        ties = {}
        for record in records[1:]:
            parts = record.split(',')
            if len(parts) < 2:
                continue
            indx = int(parts[2])
            if indx not in ties.keys():
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
            for i in range(5, 17):
                correct += int(parts[i])
            if correct == 0:
                continue
            place = int(parts[2])
            pct = get_percentile(total, place, ties[place])
            all_csv_in(hicsv, correct, pct, parts, operator.gt)
            all_csv_in(locsv, correct, pct, parts, operator.lt)
        return [hicsv, locsv]
    return False
