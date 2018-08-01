#!/usr/bin/python
"""
Write about me. To execute me try:
    python data_quality_high_level.py
"""

from collections import OrderedDict
from six import iteritems

from db_modules import couch
from settings import COUCH

from criteria import CRITERIA

# BEGIN RS FUNCTIONS ==================================================
# Adapted from the DQHL run selection checks provided by E. Falk (E.Falk@sussex.ac.uk)  4 Jun, 2017

# --- From dqtriggerproc: ---

def rsMissingGTIDCheckOK(triggerProc):
    passChecks = 0
    if len(triggerProc['check_params']['missing_gtids']) <= CRITERIA['kAmendedMaxMissGTIDCount']:
        passChecks = 1
    return passChecks

def modifBitFlipGTIDCountOK(triggerProc):
    bitFlipCountCheck = triggerProc['triggerProcBitFlipGTID']
    bitFlipCountCheck = 0
    bitFlipCount = len(triggerProc['check_params']['bitflip_gtids'])
    if ((bitFlipCount <= CRITERIA['kAmendedMaxBitFlipCount']) and
        (bitFlipCount >= 0)):
        bitFlipCountCheck = 1
    return bitFlipCountCheck

def triggerProcChecksOK(triggerProc):
    passChecks = {
        'n100l_trigger_rate' : False,
        'esumh_trigger_rate' : False,
        'triggerProcMissingGTID' : False,
    }

    try:
        if triggerProc['n100l_trigger_rate'] == 1:
            passChecks['n100l_trigger_rate'] = True
    except:
        passChecks['n100l_trigger_rate'] = None

    try:
        if triggerProc['esumh_trigger_rate'] == 1:
            passChecks['esumh_trigger_rate'] = True
    except:
        passChecks['esumh_trigger_rate'] = None

    try:
        if rsMissingGTIDCheckOK(triggerProc) == 1:
            passChecks['triggerProcMissingGTID'] = True
    except:
        passChecks['triggerProcMissingGTID'] = None

    return passChecks

def modifTriggerProcChecksOK(runNumber, triggerProc):
    passChecks = {
        'n100l_trigger_rate' : False,
        'esumh_trigger_rate' : False,
        'bit_flip_GTID_count' : False,
    }

    if (runNumber >= 101266):
        return triggerProcChecksOK(triggerProc)

    else:
        try:
            if triggerProc['n100l_trigger_rate'] == 1:
                passChecks['n100l_trigger_rate'] = True
        except:
            passChecks['n100l_trigger_rate'] = None

        try:
            if triggerProc['esumh_trigger_rate'] == 1:
                passChecks['esumh_trigger_rate'] = True
        except:
            passChecks['esumh_trigger_rate'] = None

        try:
            if modifBitFlipGTIDCountOK(triggerProc) == 1:
                passChecks['bit_flip_GTID_count'] = True
        except:
            passChecks['bit_flip_GTID_count'] = None

        return passChecks

# --- From dqtimeproc: ---

def rsRetriggerCheckOK(timeProc):
    passCheck = 0
    if ((timeProc['retriggers'] == 1) or
        (('retriggers_value' in timeProc['check_params']) and
        (timeProc['check_params']['retriggers_value'] <= CRITERIA['kAmendedMaxRetriggerRate']))):
        passCheck = 1
    return passCheck

def modifEventRateCheckOK(timeProc):
    eventRateCheck = timeProc['event_rate']
    if (eventRateCheck == 0):
        minEventRate = timeProc['criteria']['min_event_rate']
        # deltaTEventRate = timeProc['check_params']['delta_t_event_rate']
        meanEventRate = timeProc['check_params']['mean_event_rate']
        if ((meanEventRate <= CRITERIA['kAmendedMaxEventRate']) and
            (meanEventRate >= minEventRate)):
            eventRateCheck = 1
    return eventRateCheck

def modifTimeProcChecksOK(timeProc):
    passChecks = {
        'event_rate' : False,
        'event_separation' : False,
        'retriggers' : False,
        'run_header' : False,
        '10Mhz_UT_comparrison' : False,
        'clock_forward' : False,
    }

    try:
        if modifEventRateCheckOK(timeProc) == 1:
            passChecks['event_rate'] = True
    except:
        passChecks['event_rate'] = None

    try:
        if timeProc['event_separation'] == 1:
            passChecks['event_separation'] = True
    except:
        passChecks['event_separation'] = None

    try:
        if rsRetriggerCheckOK(timeProc) == 1:
            passChecks['retriggers'] = True
    except:
        passChecks['retriggers'] = None

    try:
        if timeProc['run_header'] == 1:
            passChecks['run_header'] = True
    except:
        passChecks['run_header'] = None

    try:
        if timeProc['10Mhz_UT_comparrison'] == 1:
            passChecks['10Mhz_UT_comparrison'] = True
    except:
        passChecks['10Mhz_UT_comparrison'] = None

    try:
        if timeProc['clock_forward'] == 1:
            passChecks['clock_forward'] = True
    except:
        passChecks['clock_forward'] = None

    return passChecks

# --- From dqrunproc: ---

def runProcChecksOK(runProc):
    passChecks = {
        'run_type' : False,
        'mc_flag' : False,
        'trigger' : False,
    }

    try:
        if runProc['run_type'] == 1:
            passChecks['run_type'] = True
    except:
        passChecks['run_type'] = None

    try:
        if runProc['mc_flag'] == 1:
            passChecks['mc_flag'] = True
    except:
        passChecks['mc_flag'] = None

    try:
        if runProc['trigger'] == 1:
            passChecks['trigger'] = True
    except:
        passChecks['trigger'] = None

    return passChecks

def modifRunProcChecksOK(runNumber, runProc):
    passChecks = {
        'run_type' : False,
        'mc_flag' : False,
    }

    if (runNumber >= 100600):
        return runProcChecksOK(runProc)
    else:
        try:
            if runProc['run_type'] == 1:
                passChecks['run_type'] = True
        except:
            passChecks['run_type'] = None

        try:
            if runProc['mc_flag'] == 1:
                passChecks['mc_flag'] = True
        except:
            passChecks['mc_flag'] = None

    return passChecks

# --- From dqpmtproc: ---

def pmtProcChecksOK(pmtProc):
    passChecks = {
        'general_coverage' : False,
        'crate_coverage' : False,
        'panel_coverage' : False,
    }

    try:
        if pmtProc['general_coverage'] == 1:
            passChecks['general_coverage'] = True
    except:
        passChecks['general_coverage'] = None

    try:
        if pmtProc['crate_coverage'] == 1:
            passChecks['crate_coverage'] = True
    except:
        passChecks['crate_coverage'] = None

    try:
        if pmtProc['panel_coverage'] == 1:
            passChecks['panel_coverage'] = True
    except:
        passChecks['panel_coverage'] == None

    return passChecks

# END RS FUNCTIONS ====================================================

def check(run_id):
    '''Get the basic DQHL information from CouchDB.
    '''

    # run_id = args.run_number

    data = couch.get_data(COUCH, run_id)

    if data == 1:
        context = {
            'error' : data,
            # 'error' : response['error'],
            # 'pass' : False,
        }
    else:
        checks = {}
        checks['values'] = {}
        checks['criteria'] = {}
        checks['results'] = {}

        if data != None:
            results = data['checks']

            try:
                checklist = modifTriggerProcChecksOK(int(run_id), results['dqtriggerproc'])
                if all(val==True for val in checklist.values()):
                    checks['results']['Trigger Processor'] = True
                else:
                    checks['results']['Trigger Processor'] = checklist
            except:
                pass

            try:
                checklist = modifTimeProcChecksOK(results['dqtimeproc'])
                if all(val==True for val in checklist.values()):
                    checks['results']['Time Processor'] = True
                else:
                    checks['results']['Time Processor'] = checklist
            except:
                pass

            try:
                checklist = modifRunProcChecksOK(int(run_id), results['dqrunproc'])
                if all(val==True for val in checklist.values()):
                    checks['results']['Run Processor'] = True
                else:
                    checks['results']['Run Processor'] = checklist
            except:
                pass

            try:
                checklist = pmtProcChecksOK(results['dqpmtproc'])
                if all(val==True for val in checklist.values()):
                    checks['results']['PMT Processor'] = True
                else:
                    checks['results']['PMT Processor'] = checklist
            except:
                pass

            # DQHL module decision
            status = True
            for key, value in iteritems(checks['results']):
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
