import json
import os
import unittest

from unittest.mock import MagicMock

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types


class WaterHeaterTests(unittest.TestCase):

    def setUp(self):
        super(WaterHeaterTests, self).setUp()
        self.api_interface = MagicMock()

    def test_current_state(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertEqual(water_heater.state(), "eco")

    def test_current_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertEqual(water_heater.current_set_point(), 48.888888888888886)

    def test_water_heater_modes(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertEqual(water_heater.modes(), ["eco", "heat_pump", "high_demand", "electric_only"])

    def test_water_heater_max_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertEqual(water_heater.max_set_point(), 60.0)

    def test_water_heater_min_set_point(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertEqual(water_heater.min_set_point(), 43.333333333333336)

    def test_water_heater_is_on(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertTrue(water_heater.is_on())

    def test_vacation_mode_not_enabled(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertFalse(water_heater.vacation_mode_enabled())

    def test_rheem_type(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/water_heater.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        water_heater = get_devices_from_response_dict(response_dict, device_types.WATER_HEATER)[0]
        self.assertEqual(water_heater.rheem_type(), "Heat Pump Water Heater")
