import unittest
from unittest import TestCase

from mock import patch

from app import FILENAME, load_json_file, format_time, get_business_hours

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


class TestBusinessHourDisplay(TestCase):
    """Very short test cases for busineshour formatter """
    def test_json_loader(self):
        """Test that json file loader loads json file correctly """
        self.assertEqual(DUMMY_PARSED_JSON, load_json_file(FILENAME))
        self.assertRaises(IOError, load_json_file, 'adfasdf')

    def test_format_time(self):
        """Test that seconds is converted into required time format i.e 6 pm"""
        self.assertEqual(TIME, format_time(30000))
        self.assertEqual(None, format_time('sadfasd'))

    @patch('app.load_json_file', return_value=DUMMY_PROCESSD_HOURS)
    @patch('app.process_hours', return_value=DUMMY_UNSORTED_PROCESSED_DATA)
    def test_get_business_hours(self, json_loader, hour_processor):
        """Test that hour processor return list of tuples of hours"""
        self.maxDiff = None
        self.assertEqual(DUMMY_ORDERED_DATA, get_business_hours())

    @patch('app.load_json_file', return_value=DUMMY_PROCESSD_HOURS)
    @patch('app.process_hours', return_value=None)
    def test_businss_hour_fails(self, json_loader, hour_processor):
        """Test that error displayed when no unsorted data present"""
        expected_response = {'success': False, 'message': 'Please provide the time data'}
        self.assertEqual(expected_response, get_business_hours())

    @patch('app.load_json_file', return_value=None)
    @patch('app.process_hours', return_value=DUMMY_UNSORTED_PROCESSED_DATA)
    def test_get_business_hours(self, json_loader, hour_processor):
        """Test that hour processor return list of tuples of hours"""
        expected_response = {'success': False, 'message': 'Data not found , Empty Json File'}
        self.maxDiff = None
        self.assertEqual(expected_response, get_business_hours())


if __name__ == '__main__':
    unittest.main()
