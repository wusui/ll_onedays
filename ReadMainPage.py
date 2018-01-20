#!/usr/bin/python
from html.parser import HTMLParser
import os
import requests
from CommonStuff import LLCSV_LOCATION

class MainParse(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.counter = 0
        self.data = []
        self.results = []
    def handle_starttag(self, tag, attrs):
        if tag == 'a':
            for apt in attrs:
                if apt[0] == 'href':
                    if apt[1].startswith('/oneday'):
                        self.data = [apt[1]]
                        self.counter = 2
    def handle_endtag(self, tag):
        if tag == 'a':
            if len(self.data) > 2:
                self.results.append(self.data)
            self.data = []
    def handle_data(self, data):
        if self.counter > 0:
            self.counter -= 1
            self.data.append(data)

def MainRead():
    mtext = u"https://learnedleague.com/oneday"
    r = requests.get(mtext)
    parser = MainParse()
    parser.feed(r.text)
    return parser.results

if __name__ == '__main__':
    result = MainRead()
    print(result)
    ofile = os.sep.join([LLCSV_LOCATION, "test.out"])
    with open(ofile, "w") as f:
        for linev in result:
            f.write(":".join(linev))
            f.write("\n")
