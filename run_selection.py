#!/usr/bin/python
"""
Write about me. To execute me try:
    python run_selection.py
"""

import argparse
# from datetime import datetime
import sys

import checks
# import settings

def main():
    """
    Main Run Selection script
    """

    # Define arguments
    parser = argparse.ArgumentParser()
    parser.add_argument('--date', '-d', type=str, default='',
                        dest='date', required=False,
                        help='The date of the RS shift, in dd/mm/yyyy format.')
    parser.add_argument('--name', '-n', type=str, default='',
                        dest='name', required=False,
                        help='The name associated with the RS shift.')
    parser.add_argument('--run', '-r', type=int, default=None,
                        dest='run_number', required=False,
                        help='The target run number.')
    parser.add_argument('--range', '-R', type=list, default=[100000,100001],
                        dest='range', required=False,
                        help='The date of the RS shift, in dd/mm/yyyy format.')
    parser.add_argument('--type', '-t', type=str, default='physics',
                        dest='run_type', required=False,
                        help='The run type.')
    parser.add_argument('--logfile', '-l', type=str, default='run_selection',
                        dest='logfile', required=False,
                        help='The log file.')

    # Parse arguments
    args = parser.parse_args()
    print(args)
    # return 0

    # Print the arguments back to the user as confirmation

    # Initialize the program
    # date = datetime.strptime(args.date, '%d/%m/%Y')

    # Call the checks
    print(checks.checks(args))

    # Write the checks

    # Upload the checks

if __name__ == '__main__':
    main()
