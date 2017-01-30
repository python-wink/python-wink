import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types


class LeakSmartTests(unittest.TestCase):

    def setUp(self):
        super(LeakSmartTests, self).setUp()
        self.api_interface = mock.MagicMock()
        device_list = []
        self.response_dict = {}
        _json_file = open('{}/api_responses/leaksmart_valve.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        self.response_dict["data"] = device_list

    def test_siren_state(self):
        binary_switches = get_devices_from_response_dict(self.response_dict, device_types.BINARY_SWITCH)
        for switch in binary_switches:
            if switch.model_name() == "leakSMART Valve":
                self.assertTrue(switch.state())

    def test_last_event(self):
        binary_switches = get_devices_from_response_dict(self.response_dict, device_types.BINARY_SWITCH)
        for switch in binary_switches:
            if switch.model_name() == "leakSMART Valve":
                self.assertEqual(switch.last_event(), "monthly_cycle_success")
