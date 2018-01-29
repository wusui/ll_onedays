#!/usr/bin/python
"""
Extract individual user data if it is in a csv file.
"""
import requests


def extract_csv(filen, player):
    """
    Extract individual user data if it is in a csv file.

    Input:
        filen -- csv file to be read (http address)
        player -- player name.

    Returns:
        A record containing three values.
        1. A list of player information.  This consists of:
            a. finishing position
            b. name
            c. number of questions answered correctly
        2. Total number of players in this quiz.
        3. The number of players that this person tied.
    """
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
