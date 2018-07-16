#!/usr/bin/python
"""
Write about me. To execute me try:
    python checks.py
"""

from rs_modules import run_state
from rs_modules import data_quality_low_level as dqll
# from rs_modules import data_quality_high_level as dqhl
# from rs_modules import shift_report

def checks(args):
    """
    Describe me
    """
    # print(args)

    context = {}
    context['state'] = run_state.check(args)
    context['dqll'] = dqll.check(args)
    # context['dqll'] = dqll.check(args)
    # context['shift_report'] = shift_report.check(args)

    return context

def main():
    """
    Describe me
    """

if __name__ == '__main__':
    main()
