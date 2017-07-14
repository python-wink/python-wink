import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.garage_door import WinkGarageDoor


class GarageDoorTests(unittest.TestCase):

    def setUp(self):
        super(GarageDoorTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_tamper_detected_is_false(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.GARAGE_DOOR)
        self.assertEqual(len(devices), 1)
        for device in devices:
            self.assertFalse(device.tamper_detected())

    def test_state_is_0(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.GARAGE_DOOR)
        self.assertEqual(len(devices), 1)
        for device in devices:
            self.assertEqual(device.state(), 0)

