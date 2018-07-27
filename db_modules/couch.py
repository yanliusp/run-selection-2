#!/usr/bin/python
"""
Write about me. To execute me try:
    python couch.py
"""
import requests
# import json

def get_data(DB, run_id):
    connection_details = ''
    connection_details += DB['READ']['USER']
    connection_details += ':'
    connection_details += DB['READ']['PASS']

    headers = {}
    headers['Content-type']  = 'application/json'
    headers['Authorization'] = 'Basic {}'.format((connection_details.encode('base64')).rstrip())

    url = '{}/data-quality/_design/data-quality/_view/runs'.format(DB['HOST'])

    params = {
        'descending' : 'true',
        'key' : run_id,
        'include_docs' : 'true',
    }

    data = None
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()['rows'][0]['doc']
        # data = response
    except requests.exceptions.RequestException as e:
        return {'error' : e}
    except Exception as e:
        data = {'pass': False}
        data['exception'] = e
        return data

    # if data is not None:
    #     print 'RESULT:', data
    # else:
    #     print 'ERROR'

    # return  { 'request': r }
    return data

def main():
    """
    Describe me
    """

if __name__ == '__main__':
    main()
