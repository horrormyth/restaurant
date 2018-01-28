import os

# APP CONSTANTS
SRC_DIR = os.path.abspath(os.path.dirname(__file__))
DATA_DIR = os.path.join(SRC_DIR, 'data')
FILENAME = os.path.join(DATA_DIR, 'data.json')
SORT_ORDER = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# TEST CONSTANTS

DUMMY_PARSED_JSON = \
    {u'monday': [],
     u'tuesday': [{u'type': u'open', u'value': 36000},
                  {u'type': u'close', u'value': 64800}],
     u'friday': [],
     u'wednesday': [],
     u'thursday': [{u'type': u'open', u'value': 36000},
                   {u'type': u'close', u'value': 64800}],
     u'sunday': [
         {u'type': u'open', u'value': 43200},
         {u'type': u'close', u'value': 75600},
         {u'type': u'open', u'value': 43000},
         {u'type': u'close', u'value': 64800}],
     u'saturday': [{u'type': u'open', u'value': 36000},
                   {u'type': u'close', u'value': 72000}]}
DUMMY_PROCESSD_HOURS = {u'monday': [],
                        u'tuesday': [{u'type': u'open', u'value': 36000}, {u'type': u'close', u'value': 64800}],
                        u'friday': [], u'wednesday': [],
                        u'thursday': [{u'type': u'open', u'value': 36000}, {u'type': u'close', u'value': 64800}],
                        u'sunday': [{u'type': u'open', u'value': 43200}, {u'type': u'close', u'value': 75600},
                                    {u'type': u'open', u'value': 43000}, {u'type': u'close', u'value': 64800}],
                        u'saturday': [{u'type': u'open', u'value': 36000}, {u'type': u'close', u'value': 72000}]}

DUMMY_UNSORTED_PROCESSED_DATA = {u'Monday': 'Closed',
                                 u'Tuesday': '10 AM - 6 PM',
                                 u'Friday': 'Closed',
                                 u'Wednesday': 'Closed', u'Thursday': '10 AM - 6 PM',
                                 u'Sunday': '12 PM - 9 PM, 11:56 AM - 6 PM',
                                 u'Saturday': '10 AM - 8 PM'}

DUMMY_ORDERED_DATA = {
    'business_hour': ['Monday: Closed',
                      'Tuesday: 10 AM - 6 PM',
                      'Wednesday: Closed',
                      'Thursday: 10 AM - 6 PM',
                      'Friday: Closed',
                      'Saturday: 10 AM - 8 PM',
                      'Sunday: 12 PM - 9 PM, 11:56 AM - 6 PM'],
    'success': True
}

TIME = '8:20 AM'
