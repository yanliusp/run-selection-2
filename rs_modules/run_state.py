#!/usr/bin/python
"""
Write about me. To execute me try:
    python run_state.py
"""

import datetime

from db_modules import postgres
from settings import DETECTOR

from criteria import CRITERIA
from models import RUN_TYPES

def check(args):
    """Get the basic run state information from the PostgreSQL DETECTOR database.
    """

    run_id = args.run_number
    query = 'select * from run_state where run = %i' % int(run_id)
    data = postgres.get_data(DETECTOR, query)

    if data == 1:
        context = {
            'error' : data,
        }
    else:
        checks = {}
        checks['values'] = {}
        checks['criteria'] = {}
        checks['results'] = {}

        # Calculate run duration from start and end timestamps
        if data['end_timestamp']:
            checks['values']['duration'] = \
                data['end_timestamp'] - data['timestamp']
        else:
            checks['values']['duration'] = 'In progress'

        # Build the list of set run type bits
        run_bits_flags = []
        for j in range(len(RUN_TYPES)):
            if data['run_type'] & (1<<j):
                run_bits_flags.append(RUN_TYPES[j])
        checks['values']['run_types'] = run_bits_flags

        # Run State Checks
        # 1. Physics run type bit
        if (data['run_type'] & (1 << 2)):
            checks['results']['physics'] = True
        else:
            checks['results']['physics'] = False

        # 2. Run type bits
        # The set bits check includes physics. The previous check for physics should be removed.
        if (len(set(run_bits_flags).difference(CRITERIA['run_types'])) == 0):
            checks['results']['run_type'] = True
        else:
            checks['results']['run_type'] = False

        # 3. Run duration equal to or greater than 30 minutes
        if (isinstance(checks['values']['duration'], datetime.timedelta) and
            (checks['values']['duration'].total_seconds() >= CRITERIA['kMinRunDuration'])):
            checks['results']['duration'] = True
        else:
            checks['results']['duration'] = False

        # Run State module decision
        status = True
        for check, result in checks['results'].iteritems():
            if result != True:
                status = False
                break
        checks['results']['pass'] = status # All checks have passed only after the last loop

        context = {
            'data': data,
            'checks': checks
        }

    return context

def main():
    """
    Describe me
    """

if __name__ == '__main__':
    main()
