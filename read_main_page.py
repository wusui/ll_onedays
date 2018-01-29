#!/usr/bin/python
"""
Scan the learned league oneday page for the html addresses of all quizzes.
"""
from html.parser import HTMLParser
import requests


class MainParse(HTMLParser):
    """
    HTMLParser implemented to scan the learnedleague page of oneday events
    """
    # pylint: disable=W0223
    def __init__(self):
        """
        All results are saved in self.results. Data cvurrently being scanned is
        in self.data
        """
        HTMLParser.__init__(self)
        self.counter = 0
        self.data = []
        self.results = []

    def handle_starttag(self, tag, attrs):
        """
        Save oneday html name and setup scanning for the quiz name.
        """
        if tag == 'a':
            for apt in attrs:
                if apt[0] == 'href':
                    if apt[1].startswith('/oneday'):
                        self.data = [apt[1]]
                        self.counter = 2

    def handle_endtag(self, tag):
        """
        When finsishing scanning a quiz name, make sure to save the information
        collected into self.reults.
        """
        if tag == 'a':
            if len(self.data) > 2:
                self.results.append(self.data)
            self.data = []

    def handle_data(self, data):
        """
        Using counter, make sure that the second piece of data found is saved.
        """
        if self.counter > 0:
            self.counter -= 1
            self.data.append(data)


def main_read():
    """
    Scan the learned league oneday page for all oneday quizzes.

    Return:
        A list of html addresses for all quizzes.
    """
    mtext = u"https://learnedleague.com/oneday"
    reqwest = requests.get(mtext)
    parser = MainParse()
    parser.feed(reqwest.text)
    return parser.results
