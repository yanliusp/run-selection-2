#!/usr/bin/python
"""
Write about me. To execute me try:
    python ping_crates.py
"""

# import json
from collections import OrderedDict
from six import iteritems

from db_modules import postgres
from settings import NEARLINE

from criteria import CRITERIA

def check(run_id):
    '''Get the basic Ping Crates information from the PostgreSQL NEARLINE database.
    '''

    # run_id = args.run_number
    query = """
        SELECT status, n100_crates_failed, n20_crates_failed
        FROM ping_crates
        WHERE run = %i
        ORDER BY timestamp DESC
        LIMIT 1
        """ % int(run_id)
    data = postgres.get_data(NEARLINE, query)
    # data = postgres.get_data(NEARLINE, query)[0]
    if len(data) == 1:
        data = data[0]

    if data == 1:
        context = {
            'error' : data,
        }
    else:
        checks = {}
        checks['values'] = {}
        checks['criteria'] = {}
        checks['results'] = {}

        # Ping Crates Checks
        # 1. N100 check
        try:
            #
            if len(data['n100_crates_failed']) == CRITERIA['MAX_PING_CRATES_FAILED']:
                checks['results']['n100'] = True
            else:
                checks['results']['n100'] = False
        except:
            checks['results']['n100'] = None

        # 1. N100 check
        try:
            # 
            if len(data['n20_crates_failed']) == CRITERIA['MAX_PING_CRATES_FAILED']:
                checks['results']['n20'] = True
            else:
                checks['results']['n20'] = False
        except:
            checks['results']['n20'] = None

        # Ping Crates module decision
        status = True
        for key, value in iteritems(checks['results']):
            if value != True: # There are failed checks
                status = False
                break
        checks['results']['pass'] = status

        context = {
            'data': data,
            # 'checks': checks
            'checks': OrderedDict(sorted(checks.items()))
        }

    return context

def main():
    """
    Describe me
    """

if __name__ == '__main__':
    main()
