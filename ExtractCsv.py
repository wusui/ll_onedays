#!/usr/bin/python
import os
from CommonStuff import LLCSV_LOCATION

def ExtractCsv(filen, player):
    try:
        with open(filen) as f:
            data = f.read()
            floc = data.find(',%s,' % player)
            if floc < 0:
                return False
            frest = data[floc:]
            tiev = 0
            posno = frest.split(',')[2]
            records = data.split('\n')
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
                    for i in range(5,17):
                        correct += int(parts[i])
            return [[int(posno), player, correct], len(records)-2, tiev]
    except FileNotFoundError:
        print("%s does not exist -- probably an error" % filen)
    return False

if __name__ == '__main__':
    testlist = ['lifeonearth',
                'ogdennash',
                'algorithms',
                '90salternativemusic']
    for filev in testlist:
        fullpath = os.sep.join([LLCSV_LOCATION, filev])
        fullpath = ''.join([fullpath, '.csv'])
        from CommonStuff import HELLO_MY_NAME_IS
        result = ExtractCsv(fullpath, HELLO_MY_NAME_IS)
        print(result)
