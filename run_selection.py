#!/usr/bin/python
"""
Write about me. To execute me try:
    python run_selection.py
"""

import argparse
from datetime import datetime, timedelta
import sys

import checks
from zz_modules import write
# import zz_modules import upload
from db_modules import postgres
from settings import DETECTOR, RSDB
from models import RS_MEMBERS

try:
   input = raw_input
except NameError:
   pass

def main():
    """
    Main Run Selection script
    """

    # TODO: Move the parser into a function
    # Define arguments
    parser = argparse.ArgumentParser()
    # parser = argparse.ArgumentParser(
    #     prog='PROG',
    #     formatter_class=argparse.RawDescriptionHelpFormatter,
    #     description=textwrap.dedent(
    #         '''\
    #         Give more detail!
    #         -----------------
    #             - ...
    #             - ...
    #         '''
    #         )
    #     )
    parser.add_argument('--operation', '-o', type=str, default='do',
                        choices=['do', 'wr', 'up'],
                        dest='operation', required=True,
                        help='The RS operation to perform.')
    parser.add_argument('--name', '-n', type=str, default=None, nargs=1,
                        choices=RS_MEMBERS,
                        dest='name', required=False,
                        help='The name associated with the RS shift.')
    # parser.add_argument('--date', '-d', type=str, default=None,
    #                     dest='date', required=False,
    #                     help='The date of the RS shift, in dd/mm/yyyy format.')
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--date', '-d', default=None,
                        type=lambda s: datetime.strptime(s, '%Y/%m/%d'),
                        dest='date', required=False,
                        help='The date of the RS shift, in yyyy/mm/dd format.')
    # TODO: --run and --list should be one input --runs with nargs='+'
    group.add_argument('--run', '-r', type=int, default=None, nargs=1,
                        dest='run_number', required=False,
                        help='The target run number.')
    group.add_argument('--list', '-l', type=int, default=None, nargs='+',
                        dest='run_list', required=False,
                        help='List of runs from command line (e.g. 100000 111123 116123 - runs separated by a space).')
    group.add_argument('--file', '-f', type=argparse.FileType('r'),
                        default=None, nargs='?',
                        # default=sys.stdin,
                        dest='file', required=False,
                        help='File with list of runs, one run per line.')
    group.add_argument('--range', type=int, default=None, nargs=2,
                        dest='run_range', required=False,
                        help='Begining and ending run numbers of a range. It is interpreted as a closed interval.')
    parser.add_argument('--type', '-t', type=str, default='physics',
                        dest='run_type', required=False,
                        help='The run type.')
    parser.add_argument('--logfile', type=str, default='run_selection',
                        dest='logfile', required=False,
                        help='The log file.')
    parser.add_argument('--debug', type=bool, default=False,
                        dest='debug', required=False,
                        help='Debug state.')

    # TODO: Move the validation into a function
    # Parse arguments
    print("Input parameters:")
    args = parser.parse_args()

    # Print the arguments back to the user as confirmation
    for key, value in vars(args).items():
        if value is not None:
            print("\t %s = %s" % (key, str(value)))
            if key is 'file':
                # print('Raw input: {}' % args.file.readlines())
                run_list = args.file.readlines()
                print('\tRaw input: %s' % str(run_list))
    # print(type(args), args)
    # print(vars(args))
    # return 0
    confirmation = input('Do you confirm? Answer with Y/ANY. ANSWER: ')
    if confirmation in ('Y', 'y', True):
        pass
    else:
        print('Exiting ...')
        return 0

    # Doing, (writing,) and uploading the checks should happend by executing the script for each one. This hussle is required as a precoutionary measure for good run selection reporting.

    # TODO: remove valid_list logic since the group parser object handles that
    valid_list = 0
    if args.run_number is not None:
        valid_list += 1
        # check if if it matches the run_type (defaults to physics)
        query = """
            SELECT run
            FROM run_state
            WHERE run = %i
            AND run_type & 4 > 1
            """ % int(args.run_number[0])
        # print(query)
        # return 0
        runs = postgres.get_data(DETECTOR, query)
        # print(type(runs), runs)

    if args.run_list is not None:
        valid_list += 1
        query = """
            SELECT run
            FROM run_state
            WHERE run IN %s
            AND run_type & 4 > 1
            """ % str(tuple(args.run_list))
        # print(query)
        # return 0
        runs = postgres.get_data(DETECTOR, query)
        # print(type(runs), runs)

    if args.run_range is not None:
        valid_list += 1
        range = args.run_range
        range.sort()
        # print(type(range), range)
        # get a list of physics runs from that range
        query = """
            SELECT run
            FROM run_state
            WHERE run BETWEEN %s AND %s
            AND run_type & 4 > 1
            """ % tuple(range)
        # print(query)
        # return 0
        runs = postgres.get_data(DETECTOR, query)
        # print(type(runs), runs)

    if args.date is not None:
        valid_list += 1
        # t1 = datetime.strptime(args.date, "%d/%m/%Y")
        t1 = args.date
        t2 = t1 + timedelta(days=1)
        # get a list of physics runs for that date
        query = """
            SELECT run
            FROM run_state
            WHERE timestamp > '%s' AND timestamp < '%s'
            AND run_type & 4 > 1
            ORDER BY run ASC
            """ % (t1, t2)
        # print(query)
        # return 0
        runs = postgres.get_data(DETECTOR, query)
        # print(type(runs), runs)
        # return 0

    if args.file is not None:
        valid_list += 1
        # run_list = args.file.readlines()
        # print(type(run_list), run_list)
        parsed_list = [int(x.strip('\n')) for x in run_list]
        # print(parsed_list)
        query = """
            SELECT run
            FROM run_state
            WHERE run IN %s
            AND run_type & 4 > 1
            """ % str(tuple(parsed_list))
        # print(query)
        # return 0
        runs = postgres.get_data(DETECTOR, query)
        # print(type(runs), runs)
        # return 0

    if valid_list == 1:
        pass
    else:
        if valid_list == 0:
            print('One of the --run, --list, --range, or --date arguments is required.')
        else:
            print('Only one of the --run, --list, --range, or --date arguments is required.')
        # parser.print_help()
        parser.print_usage()
        return 0

    # TODO: This part should have the logic of execution for all expected run selection operations: doing, reading/checking, uploading, testing, statistics, plots, etc.

    print('Found %i run/s maching your selection.' % len(runs))
    if len(runs) > 0:

        confirmation = input('Do you want to continue? Answer with Y/ANY. ANSWER: ')
        if confirmation in ('Y', 'y', True):
            pass
        else:
            print('Exiting ...')
            return 0

    else:
        print('Exiting ...')
        return 0

    # do = True
    wr = True
    up = False

    f = None

    # swith to case below
    # if do is True:
    if args.operation == 'do':
        # Call the checks
        size = len(runs)
        label = 'run'
        if size > 1:
            label += 's'
        print("Checking {} {}.".format(size, label))
        # return 0
        for run in sorted(runs):
            # checks.checks(args)
            # print(type(run), run, run['run'])
            print("Checking run {}.".format(int(run['run'])))
            result = checks.checks(int(run['run']))
            # print(result)

            if wr is True:
                # Write the checks
                if size < len(runs):
                    first_run = False
                else:
                    first_run = True
                size -= 1
                f = write.for_upload(run['run'], result, first_run)
                # print("Writing run {}.".format(int(run['run'])))
                # write.for_upload(result)

    elif args.operation == 'up':
        # Upload the checks
        print("Uploading ...")
        postgres.upload_csv(RSDB)
    else:
        print("Required ...")

    return 0

if __name__ == '__main__':
    main()
