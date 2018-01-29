#!/usr/bin/python
"""
Format the html output to be displayed in html pages showing best and worst
resutls.
"""
HEADER_PARTS = ['<table border="1">',
                '<tr><td> #Correct</td>',
                '<td>Best Finish</td>',
                '<td>Worst Finish</td>',
                '</tr><br />']
HEADER = ''.join(HEADER_PARTS)
LINE_TEMPLATE = '<tr><td>%d</td><td>%d pctile</td><td>%d pctile</td></tr>'


def make_table(hival, loval, outfile, use_brackets):
    """
    Input:
        hival -- dictionary of hival values (see main.py for their use)
        loval -- dictionary of loval values (see main.py for their use)
        outfile -- output file name
        use_brackets -- if true, replace '<' with '[' and '>' with ']'.
                        This is used to format talbes for message text that
                        requires the use of brackets.
    """
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
