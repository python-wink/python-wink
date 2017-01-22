import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.hub import WinkHub


class HubTests(unittest.TestCase):

    def setUp(self):
        super(HubTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
            device_list.append(json.load(_json_file))
            _json_file.close()
        self.response_dict["data"] = device_list

    def test_unit_should_be_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.HUB)
        for device in devices:
            self.assertIsNone(device.unit())

    def test_kidde_radio_code_should_not_be_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.HUB)
        for device in devices:
            if device.manufacturer_device_model() == "wink_project_one":
                continue
            if device.manufacturer_device_model() == "philips":
                continue
            else:
                self.assertIsNotNone(device.kidde_radio_code())

    def test_update_needed_is_false(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.HUB)
        for device in devices:
            self.assertFalse(device.update_needed())

    def test_ip_address_is_not_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.HUB)
        for device in devices:
            if device.manufacturer_device_model() == "philips":
                continue
            else:
                self.assertIsNotNone(device.ip_address())

    def test_firmware_version_is_not_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.HUB)
        for device in devices:
            if device.manufacturer_device_model() == "philips":
                continue
            else:
                self.assertIsNotNone(device.firmware_version())

