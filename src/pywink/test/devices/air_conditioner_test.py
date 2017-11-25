import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types


class AirConditionerTests(unittest.TestCase):

    def setUp(self):
        super(AirConditionerTests, self).setUp()
        self.api_interface = MagicMock()

    def test_ac_state(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertEqual(ac.state(), "auto_eco")

    def test_ac_modes(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertEqual(ac.modes(), ["auto_eco", "cool_only", "fan_only"])

    def test_ac_current_fan_speed(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertEqual(ac.current_fan_speed(), 1.0)

    def test_ac_current_temperature(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertEqual(ac.current_temperature(), 17.777777777777779)

    def test_ac_max_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertEqual(ac.current_max_set_point(), 20.0)

    def test_ac_is_on(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertFalse(ac.is_on())

    def test_schedule_enabled(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/quirky_aros.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        ac = get_devices_from_response_dict(response_dict, device_types.AIR_CONDITIONER)[0]
        self.assertTrue(ac.schedule_enabled())
