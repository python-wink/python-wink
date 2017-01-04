import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.standard import WinkFan
from pywink.devices.types import DEVICE_ID_KEYS


class FanSpeedTests(unittest.TestCase):

    def test_fan_speed_should_be_lowest(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        self.assertEqual(fan.current_fan_speed(), "lowest")

    def test_fan_speeds_should_be_present(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        speeds = fan.fan_speeds()
        self.assertTrue("lowest" in speeds)
        self.assertTrue("low" in speeds)
        self.assertTrue("medium" in speeds)
        self.assertTrue("high" in speeds)
        self.assertTrue("auto" in speeds)


class FanDirectionTests(unittest.TestCase):

    def test_fan_direction_should_be_forward(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        self.assertEqual(fan.current_fan_direction(), "forward")

    def test_fan_directions_should_be_present(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        directions = fan.fan_directions()
        self.assertTrue("forward" in directions)
        self.assertTrue("reverse" in directions)

class FanTimerTests(unittest.TestCase):

    def test_fan_timer_range_should_be_present(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        timer_range = fan.fan_timer_range()
        self.assertTrue(0 in timer_range)
        self.assertTrue(65535 in timer_range)

    def test_current_fan_timer_should_be_zero(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        self.assertEqual(fan.current_timer(), 0)


class FanStateTests(unittest.TestCase):

    def test_fan_state_is_off(self):
        with open('{}/api_responses/fan.json'.format(os.path.dirname(__file__))) as fan_file:
            response_dict = json.load(fan_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.FAN])

        fan = devices[0]
        """ :type fan: pywink.devices.standard.WinkFan """
        self.assertTrue(fan.state())
