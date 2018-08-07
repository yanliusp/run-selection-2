#!/usr/bin/python
"""
Write about me. To execute me try:
    python postgres.py
"""

import psycopg2
import csv

def get_data(DB, query_string):
    connection_details = ''
    connection_details += 'host='+DB['HOST']
    connection_details += ' port='+str(DB['PORT'])
    connection_details += ' dbname='+DB['NAME']
    connection_details += ' user='+DB['READ']['USER']
    connection_details += ' password='+DB['READ']['PASS']

    parameters = None

    c = None
    # e = None

    try:
        print('Connecting to db ...')
        c = psycopg2.connect(connection_details)
        print('You are now connected.')
        cr = c.cursor()


        query = """%s""" % query_string
        print('QUERY:', query)
        cr.execute(query, parameters)

        columns = [col[0] for col in cr.description]

        data = None
        # data = cr.fetchone()
        # data = cr.fetchall()

        try:
            data = [dict(zip(columns, row)) for row in cr.fetchall()]  # fixme
            # data = [dict(zip(columns, row)) for row in cr.fetchall()][0]  # fixme
        except Exception:
            data = {'pass': False}
            return data

        # if data is not None:
        #     print('RESULT:', data)
        # else:
        #     print('ERROR')

        # return 0
        if len(data) == 1:
            # return data[0]
            return data
        else:
            return data

    except psycopg2.OperationalError as e:
        print('The connection could not be established!')
        print('Error: ', e)
        # pass

        return 1

    except Exception as e:
        print('The connection could not be established!')
        print('Error:', e)
        # pass

        return 1

    finally:
        if c:
            c.close()
            print('The connection to rsdb is closed.')

def upload_csv(DB, filename='csv_data/default.csv'):
    connection_details = ''
    connection_details += 'host='+DB['HOST']
    connection_details += ' port='+str(DB['PORT'])
    connection_details += ' dbname='+DB['NAME']
    connection_details += ' user='+DB['WRITE']['USER']
    connection_details += ' password='+DB['WRITE']['PASS']

    parameters = None

    c = None
    # e = None

    try:
        print('Connecting to db ...')
        c = psycopg2.connect(connection_details)
        print('You are now connected.')
        cr = c.cursor()

        with open(filename, 'r') as inCSV:
            reader = csv.reader(inCSV)
            next(reader) # skip the header, first row
            for row in reader:
                query = """
                    INSERT INTO rs_report
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """
                cr.execute(query, row)
                print('QUERY:', query)

        # try:
        #     c.commit()
        # except psycopg2.DatabaseError as e:
        #     return {'Exception' : e}
        # finally:
        #     if c:
        #         c.rollback()

        c.commit()

    except psycopg2.DatabaseError as e:
        if c:
            c.rollback()
        print {'Exception' : e}

    except psycopg2.OperationalError as e:
        print('The connection could not be established!')
        print('Error: ', e)
        # pass

        return 1

    except Exception as e:
        print('The connection could not be established!')
        print('Error:', e)
        # pass

        return 1

    finally:
        if c:
            c.close()
            print('The connection to rsdb is closed.')

def main():
    """
    Describe me
    """

if __name__ == '__main__':
    main()
