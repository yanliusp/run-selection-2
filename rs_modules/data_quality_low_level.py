#!/usr/bin/python
"""
Write about me. To execute me try:
    python data_quality_low_level.py
"""

# import json
from collections import OrderedDict

from db_modules import postgres
from settings import RATDB

from criteria import CRITERIA

def check(args):
    '''Get the basic DQLL information from the PostgreSQL RATDB database.
    '''

    run_id = args.run_number
    query = """
        select d.data
        from ratdb_data d, ratdb_header_v2 h
        where d.key = h.key
        and h.run_begin = %i
        and h.type='DQLL'
        and h.index=''
        order by h.version desc, h.pass desc limit 1
        """ % int(run_id)
    data = postgres.get_data(RATDB, query)

    if data == 1:
        context = {
            'error' : data,
        }
    else:
        checks = {}
        checks['values'] = {}
        checks['criteria'] = {}
        checks['results'] = {}

        if data and len(data) > 0:
            data = data['data']

            # DQLL Checks
            # 1. Run duration equal to or greater than 30 minutes
            try:
                # Duration < 30 minutes
                if data['duration_seconds'] >= CRITERIA['kMinRunDuration']:
                    checks['results']['duration'] = True
                else:
                    checks['results']['duration'] = False
            except:
                checks['results']['duration'] = None

            # 2.1 All crates at HV
            try:
                # At least one crate HV is OFF (A supply)
                for crate_status in data['crate_hv_status_a']:
                    if crate_status == False:
                        checks['results']['Crate HV A'] = data['crate_hv_status_a']
                        break
                    checks['results']['Crate HV A'] = True
            except:
                checks['results']['Crate HV A'] = None

            # 2.2 OWLs at HV
            try:
                # OWLs are OFF (16B supply)
                if data['crate_16_hv_status_b'] == False:
                    checks['results']['Crate HV 16B'] = False
                else:
                    checks['results']['Crate HV 16B'] = True
            except:
                checks['results']['Crate HV 16B'] = None

            # 3.1 Non-zero DAC values
            try:
                # At least one DAC value is 0 (power supply A)
                for dac in data['crate_hv_dac_a']:
                    if dac == 0:
                        # checks['Crate DAC A'] = data['crate_hv_dac_a']
                        checks['results']['Crate DAC A'] = [False if x==0 else True for x in data['crate_hv_dac_a']]
                        break
                    checks['results']['Crate DAC A'] = True
            except:
                checks['results']['Crate DAC A'] = None

            # 3.2 Non-zero DAC values
            try:
                # OWLs DAC value is 0 (power supply B)
                if data['crate_16_hv_dac_b'] == 0:
                    checks['results']['Crate DAC 16B'] = False
                else:
                    checks['results']['Crate DAC 16B'] = True
            except:
                checks['results']['Crate DAC 16B'] = None

            # 4. Alarms
            try:
                #
                for alarm in data['detector_db_alarms']['HV_current_near_zero_A']:
                    if alarm == 1:
                        checks['results']['No alarm: HV current near zero A'] = [False if x==1 else True for x in data['detector_db_alarms']['HV_current_near_zero_A']]
                        break
                    checks['results']['No alarm: HV current near zero A'] = True

                #
                if data['detector_db_alarms']['HV_current_near_zero_A'][0] == 1:
                    checks['results']['No alarm: HV current near zero 16B'] = False
                else:
                    checks['results']['No alarm: HV current near zero 16B'] = True

                #
                for alarm in data['detector_db_alarms']['HV_over_current_A']:
                    if alarm == 1:
                        checks['results']['No alarm: HV over current A'] = [False if x==1 else True for x in data['detector_db_alarms']['HV_over_current_A']]
                        break
                    checks['results']['No alarm: HV over current A'] = True

                if data['detector_db_alarms']['HV_over_current_B'][0] == 1:
                    checks['results']['No alarm: HV over current 16B'] = False
                else:
                    checks['results']['No alarm: HV over current 16B'] = True

                #
                for alarm in data['detector_db_alarms']['HV_setpoint_discrepancy_A']:
                    if alarm == 1:
                        checks['results']['No alarm: HV setpoint discrepancy A'] = [False if x==1 else True for x in data['detector_db_alarms']['HV_setpoint_discrepancy_A']]
                        break
                    checks['results']['No alarm: HV setpoint discrepancy A'] = True

                if data['detector_db_alarms']['HV_setpoint_discrepancy_B'][0] == 1:
                    checks['results']['No alarm: HV setpoint discrepancy 16B'] = False
                else:
                    checks['results']['No alarm: HV setpoint discrepancy 16B'] = True

            except:
                # DQLL table version < 4
                pass

            # DQLL module decision
            status = True
            for key, value in checks['results'].iteritems():
                if value != True: # There are failed checks
                    status = False
                    break
            checks['results']['pass'] = status

        context = {
            'data': data,
            'checks': OrderedDict(sorted(checks.items()))
        }

    return context

def main():
    """
    Describe me
    """

if __name__ == '__main__':
    main()
