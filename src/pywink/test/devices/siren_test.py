import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types


class SirenTests(unittest.TestCase):

    def setUp(self):
        super(SirenTests, self).setUp()
        self.api_interface = mock.MagicMock()
        device_list = []
        self.response_dict = {}
        _json_file = open('{}/api_responses/go_control_siren.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        self.response_dict["data"] = device_list

    def test_siren_state(self):
        siren = get_devices_from_response_dict(self.response_dict, device_types.SIREN)[0]
        self.assertFalse(siren.state())

    def test_siren_mode(self):
        siren = get_devices_from_response_dict(self.response_dict, device_types.SIREN)[0]
        self.assertEqual(siren.mode(), "siren_and_strobe")

    def test_siren_auto_shutoff(self):
        siren = get_devices_from_response_dict(self.response_dict, device_types.SIREN)[0]
        self.assertEqual(siren.auto_shutoff(), 60)
