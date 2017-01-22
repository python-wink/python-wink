import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.fan import WinkFan


class FanTests(unittest.TestCase):

    def setUp(self):
        super(FanTests, self).setUp()
        self.api_interface = mock.MagicMock()
        device_list = []
        self.response_dict = {}
        _json_file = open('{}/api_responses/fan.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        self.response_dict["data"] = device_list

    def test_fan_speeds(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        has_speeds = fan.fan_speeds()
        self.assertEqual(len(has_speeds), 5)
        speeds = ['lowest', 'low', 'medium', 'high', 'auto']
        for speed in has_speeds:
            self.assertTrue(speed in speeds)

    def test_fan_directions(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        has_directions = fan.fan_directions()
        self.assertEqual(len(has_directions), 2)
        directions = ['forward', 'reverse']
        for direction in has_directions:
            self.assertTrue(direction in directions)

    def test_fan_timer_range(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        has_timer_range = fan.fan_timer_range()
        self.assertEqual(len(has_timer_range), 2)
        times = [0, 65535]
        for time in has_timer_range:
            self.assertTrue(time in times)

    def test_fan_speed_is_low(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        self.assertEqual(fan.current_fan_speed(), "lowest")

    def test_fan_direction_is_forward(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        self.assertEqual(fan.current_fan_direction(), "forward")

    def test_fan_timer_is_0(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        self.assertEqual(fan.current_timer(), 0)

    def test_fan_state(self):
        fan = get_devices_from_response_dict(self.response_dict, device_types.FAN)[0]
        self.assertTrue(fan.state())
