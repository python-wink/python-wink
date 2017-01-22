import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.light_bulb import WinkLightBulb


class LightBulbTests(unittest.TestCase):

    def setUp(self):
        super(LightBulbTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_bulb_brightness(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/lightify_rgbw_bulb.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        bulb = get_devices_from_response_dict(response_dict, device_types.LIGHT_BULB)[0]
        self.assertEqual(bulb.brightness(), 0.02)

    def test_bulb_color(self):
        device_list = []
        response_dict = {}
        _json_file = open('{}/api_responses/lightify_rgbw_bulb.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        response_dict["data"] = device_list
        bulb = get_devices_from_response_dict(response_dict, device_types.LIGHT_BULB)[0]
        self.assertFalse(bulb.supports_rgb())
        self.assertFalse(bulb.supports_xy_color())
        self.assertTrue(bulb.supports_hue_saturation())
        self.assertTrue(bulb.supports_temperature())
        self.assertEqual(bulb.color_temperature_kelvin(), 2755)
        self.assertEqual(bulb.color_hue(), 0.0)
        self.assertEqual(bulb.color_saturation(), 1.0)
