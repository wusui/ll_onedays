#!/usr/bin/python
""" TO DO: """
from html.parser import HTMLParser
import requests

class MainParse(HTMLParser):
    #pylint: disable=W0223
    """ TO DO: """
    def __init__(self):
        """ TO DO: """
        HTMLParser.__init__(self)
        self.counter = 0
        self.data = []
        self.results = []
    def handle_starttag(self, tag, attrs):
        """ TO DO: """
        if tag == 'a':
            for apt in attrs:
                if apt[0] == 'href':
                    if apt[1].startswith('/oneday'):
                        self.data = [apt[1]]
                        self.counter = 2
    def handle_endtag(self, tag):
        """ TO DO: """
        if tag == 'a':
            if len(self.data) > 2:
                self.results.append(self.data)
            self.data = []
    def handle_data(self, data):
        """ TO DO: """
        if self.counter > 0:
            self.counter -= 1
            self.data.append(data)

def main_read():
    """ TO DO: """
    mtext = u"https://learnedleague.com/oneday"
    reqwest = requests.get(mtext)
    parser = MainParse()
    parser.feed(reqwest.text)
    return parser.results
