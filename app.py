import datetime
import json
import logging
from future_builtins import zip

from constants import FILENAME, SORT_ORDER


def load_json_file(path):
    """
    Reads json file
    :param path: file path
    :return: dict
    """
    with open(path) as file_name:
        try:
            json_data = json.load(file_name)
            return json_data
        except AttributeError as e:
            logging.exception(e)
            return None


def get_business_hours():
    """
    Returns the the list of formatted hour display
    e.g
        ['Monday: Closed', 'Tuesday: 10 AM - 6 PM',
         'Wednesday: Closed', 'Thursday: 10 AM - 6 PM',
          'Friday: Closed', 'Saturday: 10 AM - 8 PM',
           'Sunday: 12 PM - 9 PM, 11:56 AM - 6 PM']
    :return:
    """
    try:
        raw_hour_data = load_json_file(FILENAME)
        # print raw_hour_data
    except IOError as error:
        logging.exception(error)
        return {'success': False, 'message': 'File not found'}
    if raw_hour_data:
        unsorted_hours = process_hours(raw_hour_data)
        if not unsorted_hours:
            return {'success': False, 'message': 'Please provide the time data'}
        sorted_hours = sorted(unsorted_hours.items(), key=lambda pair: SORT_ORDER.index(pair[0]))
        hours = [('{}: {}'.format(day, hour)) for day, hour in sorted_hours]

        return {'success': True, 'business_hour': hours}
    else:
        return {'success': False, 'message': 'Data not found , Empty Json File'}


def format_time(seconds=None):
    """
    Retruns the formatted time
    e.g
        6 pm
    :param seconds: Unix seconds e.g 64800
    :return: formatted time
    """
    try:
        hour = datetime.datetime.utcfromtimestamp(seconds)
    except (ValueError, TypeError) as error:
        logging.exception(error)
        return None
    formatted_time = hour.strftime("%I:%M %p")
    if not hour.minute:
        formatted_time = hour.strftime("%I %p")
    return formatted_time.lstrip('0')


def pairwise(iterable):
    """
    Returns tuple
    More at: https://docs.python.org/3/library/itertools.html
     s -> (s0,s1), (s1,s2), (s2, s3), ...

    :param iterable:
    :return: paired tuple
    """
    a = iter(iterable)
    return zip(a, a)


def process_hours(data_dict=None):
    """

    :param jsondata: dict of working hours
    e.g json_data = {
                    "monday": [],
                    "tuesday": [
                                {
                                    "type": "open",
                                    "value": 36000
                                },
                                {
                                    "type": "close",
                                    "value": 64800
                                }
                                ],
                    }
    :return:unsorted dict
    e.g
        data: {
                'Monday': 'Closed',
                'Tuesday': '10 AM - 6 PM',
                'Friday': 'Closed'
            }
    """

    if not data_dict or not isinstance(data_dict, dict):
        return None
    business_hours = {}
    for day, work_hours in data_dict.items():
        if not work_hours:
            business_hours[day.title()] = 'Closed'
        else:
            working_time = []
            for hours in work_hours:
                hour = hours.get('value', None)
                hour = format_time(hour)
                working_time.append('%s' % hour)
            # Utilizing working_time here again !! makes the multiple working hour a pair
            working_time = [
                ('{} - {}'.format(opening_hour, closing_hour))
                for opening_hour, closing_hour in pairwise(working_time)
            ]
            business_hours[day.title()] = ', '.join(working_time)
    return business_hours


if __name__ == '__main__':
    business_hour = get_business_hours()
    success = business_hour.get('success', False)
    if success:
        try:
            hours = business_hour['business_hour']
            for hour in hours:
                print hour
        except AttributeError as e:
            logging.exception(e)
    else:
        print(business_hour.get('message', 'Something Horribly Went Wrong Contact Support'))
