import json
import os
import unittest

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types


class PowerstripTests(unittest.TestCase):

    def test_state_powerstrip_state_should_be_true_if_one_outlet_is_true(self):
        with open('{}/api_responses/pivot_power_genius.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.POWERSTRIP)

        self.assertEqual(len(devices), 3)
        powerstrip = devices[-1]
        outlet_1 = devices[0]
        outlet_2 = devices[1]
        self.assertTrue(powerstrip.state())
        self.assertFalse(outlet_1.state())
        self.assertTrue(outlet_2.state())

    def test_outlet_parent_id_matches_powerstrip_id(self):
        with open('{}/api_responses/pivot_power_genius.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.POWERSTRIP)

        self.assertEqual(len(devices), 3)
        powerstrip = devices[-1]
        outlet_1 = devices[0]
        outlet_2 = devices[1]
        self.assertEqual(powerstrip.object_id(), outlet_1.parent_id())
        self.assertEqual(powerstrip.object_id(), outlet_2.parent_id())

    def test_outlet_index(self):
        with open('{}/api_responses/pivot_power_genius.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.POWERSTRIP)

        self.assertEqual(len(devices), 3)
        outlet_1 = devices[0]
        outlet_2 = devices[1]
        self.assertEqual(0, outlet_1.index())
        self.assertEqual(1, outlet_2.index())

    def test_outlet_parent_object_type(self):
        with open('{}/api_responses/pivot_power_genius.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.POWERSTRIP)

        self.assertEqual(len(devices), 3)
        powerstrip = devices[-1]
        outlet_1 = devices[0]
        outlet_2 = devices[1]
        self.assertEqual(powerstrip.object_type(), outlet_1.parent_object_type())
        self.assertEqual(powerstrip.object_type(), outlet_2.parent_object_type())
