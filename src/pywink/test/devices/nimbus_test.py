import json
import os
import unittest
from datetime import datetime

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types
from pywink.devices.cloud_clock import WinkCloudClock, WinkCloudClockDial, WinkCloudClockAlarm, _create_ical_string


class NimbusTests(unittest.TestCase):

    def test_cloud_clock_json_parses_into_the_correct_objects(self):
        with open('{}/api_responses/nimbus.json'.format(os.path.dirname(__file__))) as nimbus_file:
            response_dict = json.load(nimbus_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.CLOUD_CLOCK)

        self.assertEqual(len(devices), 8)
        cloud_clock = devices[0]
        self.assertTrue(isinstance(devices[0], WinkCloudClock))

        self.assertTrue(isinstance(devices[1], WinkCloudClockDial))
        self.assertTrue(isinstance(devices[2], WinkCloudClockDial))
        self.assertTrue(isinstance(devices[3], WinkCloudClockDial))
        self.assertTrue(isinstance(devices[4], WinkCloudClockDial))
        self.assertTrue(isinstance(devices[5], WinkCloudClockAlarm))
        self.assertTrue(isinstance(devices[6], WinkCloudClockAlarm))
        self.assertTrue(isinstance(devices[7], WinkCloudClockAlarm))
        self.assertEqual(devices[1].parent, cloud_clock)
        self.assertEqual(devices[2].parent, cloud_clock)
        self.assertEqual(devices[3].parent, cloud_clock)
        self.assertEqual(devices[4].parent, cloud_clock)
        self.assertEqual(devices[5].parent, cloud_clock)
        self.assertEqual(devices[6].parent, cloud_clock)
        self.assertEqual(devices[7].parent, cloud_clock)

    def test_cloud_clock_dials_have_the_correct_value(self):
        with open('{}/api_responses/nimbus.json'.format(os.path.dirname(__file__))) as nimbus_file:
            response_dict = json.load(nimbus_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.CLOUD_CLOCK)

        time_dial = devices[1]
        porkfolio_dial = devices[3]
        custom_dial = devices[4]

        self.assertEqual(time_dial.state(), 41639.0)
        self.assertEqual(porkfolio_dial.state(), 1327.0)
        self.assertEqual(custom_dial.state(), 212.0)

        self.assertEqual(time_dial.position(), 346.99166666666667)
        self.assertEqual(porkfolio_dial.position(), 296.658)
        self.assertEqual(custom_dial.position(), 212.0)

        self.assertEqual(time_dial.labels(), ["11:33 AM", "New York"])
        self.assertEqual(porkfolio_dial.labels(), ["$13.27", "PORK"])
        self.assertEqual(custom_dial.labels(), ["212"])

        self.assertEqual(time_dial.rotation(), "cw")
        self.assertEqual(porkfolio_dial.rotation(), "cw")
        self.assertEqual(custom_dial.rotation(), "ccw")

        self.assertEqual(time_dial.position(), 346.99166666666667)
        self.assertEqual(porkfolio_dial.position(), 296.658)
        self.assertEqual(custom_dial.position(), 212.0)

        self.assertEqual(time_dial.max_value(), 86400)
        self.assertEqual(porkfolio_dial.max_value(), 5000)
        self.assertEqual(custom_dial.max_value(), 360)

        self.assertEqual(time_dial.min_value(), 0)
        self.assertEqual(porkfolio_dial.min_value(), 0)
        self.assertEqual(custom_dial.min_value(), 0)

        self.assertEqual(time_dial.ticks(), 12)
        self.assertEqual(porkfolio_dial.ticks(), 12)
        self.assertEqual(custom_dial.ticks(), 12)

        self.assertEqual(time_dial.min_position(), 0)
        self.assertEqual(porkfolio_dial.min_position(), -135)
        self.assertEqual(custom_dial.min_position(), 0)

        self.assertEqual(time_dial.max_position(), 720)
        self.assertEqual(porkfolio_dial.max_position(), 135)
        self.assertEqual(custom_dial.max_position(), 360)

    def test_get_time_dial_returns_the_time_dial(self):
        with open('{}/api_responses/nimbus.json'.format(os.path.dirname(__file__))) as nimbus_file:
            response_dict = json.load(nimbus_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.CLOUD_CLOCK)

        cloud_clock = devices[0]
        time_dial = devices[1]

        self.assertEqual(cloud_clock.get_time_dial(), time_dial.json_state)

    def test_get_alarm_state_returns_the_correct_value(self):
        with open('{}/api_responses/nimbus.json'.format(os.path.dirname(__file__))) as nimbus_file:
            response_dict = json.load(nimbus_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.CLOUD_CLOCK)

        first_alarm = devices[5]
        self.assertEqual(first_alarm.state(), 1533576003)

    def test_create_ical_string(self):
        with open('{}/api_responses/nimbus.json'.format(os.path.dirname(__file__))) as nimbus_file:
            response_dict = json.load(nimbus_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.CLOUD_CLOCK)

        first_alarm = devices[5]
        the_date = datetime.strptime('20180804T233251', '%Y%m%dT%H%M%S')
        self.assertEqual(first_alarm.recurrence(), _create_ical_string("America/New_York", the_date, ["SA"]))
        self.assertEqual("DTSTART;TZID=America/New_York:20180804T233251\nRRULE:FREQ=DAILY", _create_ical_string("America/New_York", the_date, "DAILY"))
        self.assertEqual("DTSTART;TZID=America/New_York:20180804T233251\nRRULE:FREQ=WEEKLY;BYDAY=MO", _create_ical_string("America/New_York", the_date, ["TEST", "MO"]))

