import copy
import logging
import os
from logging.handlers import RotatingFileHandler

from flask import Flask, jsonify, request
from jsonschema import validate
from jsonschema.exceptions import ValidationError

from app import load_json_file
from constants import FILENAME

logger = logging.getLogger(__name__)
app = Flask(__name__)
app.config.from_object(os.environ['APP_SETTINGS'])

restaurant_hours = {}
data = load_json_file(path=FILENAME)
restaurant_hours['ravintolax'] = data

working_hours_copy = copy.deepcopy(restaurant_hours)


def abort(messsage):
    """ Generates a error message"""
    return jsonify({'Error': messsage, 'success': False})


@app.route('/api/restaurant/', methods=['GET'])
def get_all_business_hour():
    """
    Get all restauran tworking hours
    :return: json
        Jsonified list of restaurant including working hours or error
    """
    if data:
        return jsonify(restaurant_hours)
    return jsonify({'Error': 'No data found', 'code': 400})


@app.route('/api/restaurant/<name>', methods=['GET'])
def get_working_hour(name):
    """
    Get working hours of a restaurant
    :param name: string
    :return: json
        Retunrs jsonified working hours of a restaurant of error
    """
    working_hour = restaurant_hours.get(name.lower(), None)
    if not working_hour:
        return abort('Restaurant {} not found'.format(name))
    return jsonify(working_hour)


@app.route('/api/restaurant/<name>/<weekday>', methods=['GET'])
def get_working_hour_per_day(name, weekday):
    """
    Get working hours of a restaurant for a particular day
    :param name: string
    :param weekday: string
        e.g: Weekdays name
    :return: json
        Return jsonified weekday working hours or error
    """
    restaurant = restaurant_hours.get(name, None)
    if restaurant:
        try:
            working_hour = restaurant[weekday]
            return jsonify(working_hour)
        except KeyError as e:
            logger.exception(e)
            return abort('Working hours not found for the restaurant {} '.format(name)), 400
    return abort('Restaurant {} not found'.format(name))


@app.route('/api/restaurant/<name>/<weekday>', methods=['POST'])
def create_time_table(name, weekday):
    """
    Add new timetable for particular day
    POST DATA:
    {
                    "type": "close",
                    "value": 72000
                }

    :param name: string
    :param weekday: string
    :return: updated data for the restaurant
    """

    new_time = request.json()
    validator = load_json_file('time.json')
    try:
        validate(new_time, validator)
    except ValidationError as error:
        logger.exception(error)
        return abort('Invalid data found in post request ')

    try:
        working_hour = working_hours_copy[name][weekday]
    except KeyError as error:
        logger.exception(error)
        return abort('No restaurant found ')

    if not working_hour:
        working_hours_copy[name][weekday] = [new_time, ]

    if new_time in working_hour:
        return abort('Requested time table already exist, please add the new one '), 400
    working_hours_copy[name][weekday].append(new_time)
    return jsonify(working_hours_copy)


@app.route('/api/restaurant/<name>/', methods=['DELETE'])
def delete_time_table(name):
    """
    Delete particular weekday timetable
    :param name:string
    :param weekday:string
    :return:deleted timetable
    """
    logger.info('hello')
    try:
        content = request.json()
    except TypeError as error:
        logger.exception(error)
        return abort('Malmformed data found'), 404
    weekday = content.get('weekday', None)
    if not weekday:
        return abort('Please provide weekday to remove')
    try:
        deleted_item = working_hours_copy[name].pop(weekday)
    except KeyError as error:
        logger.exception(error)
        return abort('There is no day such as {}'.format(weekday))
    return jsonify({'deleted': True, 'item': deleted_item})


if __name__ == '__main__':
    formatter = logging.Formatter(
        "[%(asctime)s] {%(pathname)s:%(lineno)d} %(levelname)s - %(message)s")
    handler = RotatingFileHandler('api_logs.log', maxBytes=10000, backupCount=1)
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    app.logger.addHandler(handler)
    app.run()
