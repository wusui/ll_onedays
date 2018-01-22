#!/usr/bin/python
""" TO DO: """
HEADER_PARTS = ['<table border="1">',
                '<tr><td> #Correct</td>',
                '<td>Best Finish</td>',
                '<td>Worst Finish</td>',
                '</tr><br />']
HEADER = ''.join(HEADER_PARTS)
LINE_TEMPLATE = '<tr><td>%d</td><td>%d pctile</td><td>%d pctile</td></tr>'

def make_table(hival, loval, outfile, use_brackets):
    """ TO DO: """
    fstring = HEADER
    for i in range(1, 13):
        xrec = hival[i]['pctile']
        yrec = loval[i]['pctile']
        ostring = LINE_TEMPLATE % (i, xrec, yrec)
        ostring = ostring.replace('pctile', '%ile')
        fstring = ''.join([fstring, ostring])
    fstring = ''.join([fstring, '</table>'])
    if use_brackets:
        fstring = fstring.replace('<', '[')
        fstring = fstring.replace('>', ']')
        fstring = fstring.replace(' border="1"', '')
    with open(outfile, 'w') as filedesc:
        filedesc.write(fstring)
