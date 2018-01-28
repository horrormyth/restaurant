import unittest
from unittest import TestCase

from mock import patch

from app import load_json_file, format_time, get_business_hours
from constants import (
    DUMMY_ORDERED_DATA,
    DUMMY_UNSORTED_PROCESSED_DATA,
    DUMMY_PROCESSD_HOURS,
    DUMMY_PARSED_JSON,
    TIME,
    FILENAME
)


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
    def test_get_business_hours_fails_on_no_json(self, json_loader, hour_processor):
        """Test that hour processor returns error when no json data"""
        expected_response = {'success': False, 'message': 'Data not found , Empty Json File'}
        self.maxDiff = None
        self.assertEqual(expected_response, get_business_hours())


if __name__ == '__main__':
    unittest.main()
