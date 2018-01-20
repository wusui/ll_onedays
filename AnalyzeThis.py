#!/usr/bin/python
from html.parser import HTMLParser
import requests

class MatchParse(HTMLParser):
    def __init__(self, player):
        HTMLParser.__init__(self)
        self.iam = player
        self.counter = 0
        self.results = []
        self.playerv = []
        self.scanforPos = False
        self.scanforName = False
        self.scanforScores = False
        self.right = 0
        self.wrong = 0
        self.commented = False
        self.currentdata = []
        self.myPosition = 0

    def handle_starttag(self, tag, attrs):
        if not self.scanforPos:
            for apt in attrs:
                if apt[0] == 'class':
                    if apt[1] == 'std-midleft':
                        self.counter += 1
                        self.scanforPos = True
    def handle_data(self, data):
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
                self.currentdata.append(self.right)
                self.scanforScores = False
                if self.currentdata[1].endswith(self.iam):
                    self.playerv = self.currentdata
                    self.myPosition = self.currentdata[0]
                self.results.append(self.currentdata)
                self.right = 0
                self.wrong = 0
                self.currentdata = []
        if self.scanforName:
            if data.startswith('XXXXX:') or self.commented:
                self.currentdata.append(data)
                self.scanforPos = False
                self.scanforName = False
                self.scanforScores = True
        if self.scanforPos:
            if data.endswith('.'):
                strval = data[0:-1]
                try:
                    posis = int(strval)
                except ValueError:
                    return
                self.currentdata.append(posis)
                self.scanforName = True

def AnalyzeThis(filen, player):
    r = requests.get(filen)
    retv = False
    scanner = ['&nbsp;%s' % player, '&nbsp;-->%s' % player]
    for field in scanner:
        if field in r.text:
            retv = True
            break
    if not retv:
        return False
    parser = MatchParse(player)
    if r.text.find('&nbsp;-->') > 0:
        parser.commented = True
    our_version = r.text.split('&nbsp')
    our_text = 'XXXXX:'.join(our_version)
    parser.feed(our_text)
    tie_count = 0
    total = 0
    for plyr in parser.results:
        if plyr[0] == parser.myPosition:
            tie_count += 1
        total += 1
    return [parser.playerv, total, tie_count]

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
        from CommonStuff import HELLO_MY_NAME_IS
        result = AnalyzeThis(filev, HELLO_MY_NAME_IS)
        print(result)
