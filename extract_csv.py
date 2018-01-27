#!/usr/bin/python
""" TO DO: """
import requests


def extract_csv(filen, player):
    """ TO DO: """
    data = requests.get(filen)
    floc = data.text.find(',%s,' % player)
    if floc < 0:
        return False
    frest = data.text[floc:]
    tiev = 0
    posno = frest.split(',')[2]
    records = data.text.split('\n')
    correct = 0
    for record in records:
        parts = record.split(',')
        if parts[0] == 'Season':
            continue
        if len(parts) < 2:
            continue
        if parts[2] == posno:
            tiev += 1
        if parts[1] == player:
            for i in range(5, 17):
                correct += int(parts[i])
    return [[int(posno), player, correct], len(records)-2, tiev]
