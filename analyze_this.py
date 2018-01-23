#!/usr/bin/python
""" TO DO: """
from html.parser import HTMLParser
import requests

class MatchParse(HTMLParser):
    """ TO DO: """
    #pylint: disable=W0223
    def __init__(self, player):
        """ TO DO: """
        HTMLParser.__init__(self)
        self.iam = player
        self.results = []
        self.playerv = []
        self.scan_for = {}
        self.scan_for['pos'] = False
        self.scan_for['name'] = False
        self.scan_for['scores'] = False
        self.scan_for['commented'] = False
        self.lval = {}
        self.lval['right'] = 0
        self.lval['wrong'] = 0
        self.lval['myposition'] = 0
        self.lval['counter'] = 0
        self.currentdata = []

    def handle_starttag(self, tag, attrs):
        """ TO DO: """
        if tag in []:
            return
        if not self.scan_for['pos']:
            for apt in attrs:
                if apt[0] == 'class':
                    if apt[1] == 'std-midleft':
                        self.lval['counter'] += 1
                        self.scan_for['pos'] = True
    def handle_data(self, data):
        """ TO DO: """
        if self.scan_for['scores']:
            try:
                nval = int(data)
            except ValueError:
                print('%s is invalid numerical input' % data)
                return
            if nval == 0:
                self.lval['wrong'] += 1
            else:
                self.lval['right'] += 1
            if (self.lval['right'] + self.lval['wrong']) == 12:
                self.currentdata.append(self.lval['right'])
                self.scan_for['scores'] = False
                if self.currentdata[1].endswith(self.iam):
                    self.playerv = self.currentdata
                    self.lval['myposition'] = self.currentdata[0]
                self.results.append(self.currentdata)
                self.lval['right'] = 0
                self.lval['wrong'] = 0
                self.currentdata = []
        if self.scan_for['name']:
            if data.startswith('XXXXX:') or self.scan_for['commented']:
                self.currentdata.append(data)
                self.scan_for['pos'] = False
                self.scan_for['name'] = False
                self.scan_for['scores'] = True
        if self.scan_for['pos']:
            if data.endswith('.'):
                strval = data[0:-1]
                try:
                    posis = int(strval)
                except ValueError:
                    return
                self.currentdata.append(posis)
                self.scan_for['name'] = True

def analyze_this(filen, player):
    """ TO DO: """
    reqf = requests.get(filen)
    retv = False
    scanner = ['&nbsp;%s' % player, '&nbsp;-->%s' % player]
    for field in scanner:
        if field in reqf.text:
            retv = True
            break
    if not retv:
        return False
    parser = MatchParse(player)
    if reqf.text.find('&nbsp;-->') > 0:
        parser.scan_for['commented'] = True
    our_version = reqf.text.split('&nbsp')
    our_text = 'XXXXX:'.join(our_version)
    parser.feed(our_text)
    tie_count = 0
    total = 0
    for plyr in parser.results:
        if plyr[0] == parser.lval['myposition']:
            tie_count += 1
        total += 1
    return [parser.playerv, total, tie_count]
