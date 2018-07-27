#!/usr/bin/python
"""
Write about me. To execute me try:
    python write.py
"""

import csv

def save_results(filename, results):
    with open(filename, 'w') as f:
        csv_writer = csv.writer(f)
        # csv_writer.writerows(results)
        csv_writer.writerow(results)

def for_upload(data):

    rs_modules = ['state', 'dqll', 'dqhl']

    sHeader = ','.join(rs_modules)
    summary = []
    dHeader = []
    details = []

    for module in rs_modules:
        # print "Going through ", check
        # for key, value in data[module].items():
        #     print key
        # print type(data[module]['checks']), data[module]['checks']
        # try:
        #     print data[module]['checks']['results']
        # except:
        #     print '...'
        #     # pass

        for check, value in data[module]['checks']['results'].items():
            if check != 'pass':
                dHeader.append(check)
                details.append(value)

        summary.append(data[module]['checks']['results']['pass'])

    print "Summary ..."
    print sHeader
    print summary
    print "More info ..."
    print dHeader
    print details

    fn = "rs_test.csv"
    save_results(fn, details)

    return data

def main():
    """
    Describe me ...
    """

if __name__ == '__main__':
    main()
