#!/usr/bin/python
"""
Write about me. To execute me try:
    python write.py
"""

import os
import csv

def save_results(header, results, first, filename):
    # f_flags = 'a'
    if first:
        f_flags = 'w+'
    else:
        f_flags = 'a'

    directory = filename.split('/')[0]

    if not os.path.exists(directory):
        try:
            os.makedirs(directory)
        except Exception as e:
            return e

    with open(filename, f_flags) as f:
        csv_writer = csv.writer(f)
        # csv_writer.writerows(results)
        if first:
            csv_writer.writerow(header)

        csv_writer.writerow(results)

def for_upload(run, data, first, filename='csv_data/default.csv'):

    rs_modules = ['state', 'dqll', 'dqhl', 'muons', 'ping']

    sHeader = ','.join(rs_modules)
    summary = []
    dHeader = []
    details = []

    dHeader.append('RUNRUN')
    details.append(run)

    for module in rs_modules:
        # print("Going through ", check)
        # for key, value in data[module].items():
        #     print(key)
        # print(type(data[module]['checks']), data[module]['checks'])
        # try:
        #     print(data[module]['checks']['results'])
        # except:
        #     print('...')
        #     # pass

        for check, value in data[module]['checks']['results'].items():
            if check != 'pass':
                # dHeader.append(check)
                # dHeader.append(''.join(sorted(str(value).upper())))
                dHeader.append(module[:4])
                if value == True:
                    details.append(value)
                else:
                    details.append('FFFF')

        summary.append(data[module]['checks']['results']['pass'])

    # print("Summary ...")
    # print(sHeader)
    # print(summary)
    # print("More info ...")
    # print(dHeader)
    # print(details)

    save_results(dHeader, details, first, filename)

    return data

def main():
    """
    Describe me ...
    """

if __name__ == '__main__':
    main()
