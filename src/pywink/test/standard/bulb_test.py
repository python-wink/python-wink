import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.standard import WinkBulb
from pywink.devices.types import DEVICE_ID_KEYS


class BulbSupportsHueSaturationTest(unittest.TestCase):

    def test_should_be_true_if_response_contains_hue_and_saturation_capabilities(self):
        with open('{}/api_responses/hue_and_saturation_present.json'.format(os.path.dirname(__file__))) as light_file:
            response_dict = json.load(light_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LIGHT_BULB])

        bulb = devices[0]
        """ :type bulb: pywink.devices.standard.WinkBulb """
        supports_hs = bulb.supports_hue_saturation()
        self.assertTrue(supports_hs,
                        msg="Expected hue and saturation to be supported")

    def test_should_be_false_if_response_does_not_contain_hue_and_saturation_capabilities(self):
        with open('{}/api_responses/hue_and_saturation_absent.json'.format(os.path.dirname(__file__))) as light_file:
            response_dict = json.load(light_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LIGHT_BULB])

        bulb = devices[0]
        """ :type bulb: pywink.devices.standard.WinkBulb """
        supports_hs = bulb.supports_hue_saturation()
        self.assertFalse(supports_hs,
                        msg="Expected hue and saturation to be supported")


class BulbSupportsTemperatureTest(unittest.TestCase):

    def test_should_be_true_if_response_contains_temperature_capabilities(self):
        with open('{}/api_responses/temperature_present.json'.format(os.path.dirname(__file__))) as light_file:
            response_dict = json.load(light_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LIGHT_BULB])

        bulb = devices[0]
        """ :type bulb: pywink.devices.standard.WinkBulb """
        supports_temperature = bulb.supports_temperature()
        self.assertTrue(supports_temperature,
                        msg="Expected temperature to be supported")


    def test_should_be_false_if_response_does_not_contain_temperature_capabilities(self):
        with open('{}/api_responses/temperature_absent.json'.format(os.path.dirname(__file__))) as light_file:
            response_dict = json.load(light_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LIGHT_BULB])

        bulb = devices[0]
        """ :type bulb: pywink.devices.standard.WinkBulb """
        supports_temperature = bulb.supports_temperature()
        self.assertFalse(supports_temperature,
                        msg="Expected temperature to be un-supported")


class LightTests(unittest.TestCase):

    def setUp(self):
        super(LightTests, self).setUp()
        self.api_interface = WinkApiInterface()

    def test_should_handle_light_bulb_response(self):
        with open('{}/api_responses/light_bulb.json'.format(os.path.dirname(__file__))) as light_file:
            response_dict = json.load(light_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LIGHT_BULB])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkBulb)

    @mock.patch('requests.put')
    def test_should_send_correct_color_hsb_values_to_wink_api(self, put_mock):
        bulb = WinkBulb({
            "capabilities": {
                "fields": [
                    {
                        "field": "hue"
                    },
                    {
                        "field": "saturation"
                    }
                ],
                "color_changeable": True
            }
        }, self.api_interface)
        hue = 0.75
        saturation = 0.25
        bulb.set_state(True, color_hue_saturation=[hue, saturation])
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals(hue, sent_data.get('desired_state', {}).get('hue'))
        self.assertEquals(saturation, sent_data.get('desired_state', {}).get('saturation'))
        self.assertEquals('hsb', sent_data['desired_state'].get('color_model'))

    @mock.patch('requests.put')
    def test_should_send_correct_color_temperature_values_to_wink_api(self, put_mock):
        bulb = WinkBulb({
            "capabilities": {
                "fields": [
                    {
                        "field": "color_temperature"
                    }
                ],
                "color_changeable": True
            }
        }, self.api_interface)
        arbitrary_kelvin_color = 4950
        bulb.set_state(True, color_kelvin=arbitrary_kelvin_color)
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals('color_temperature', sent_data['desired_state'].get('color_model'))
        self.assertEquals(arbitrary_kelvin_color, sent_data['desired_state'].get('color_temperature'))

    @mock.patch('requests.put')
    def test_should_only_send_color_hsb_if_both_color_hsb_and_color_temperature_are_given(self, put_mock):
        bulb = WinkBulb({
            "capabilities": {
                "fields": [
                    {
                        "field": "hue"
                    },
                    {
                        "field": "saturation"
                    }
                ],
                "color_changeable": True
            }
        }, self.api_interface)
        arbitrary_kelvin_color = 4950
        bulb.set_state(True, color_kelvin=arbitrary_kelvin_color, color_hue_saturation=[0, 1])
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals('hsb', sent_data['desired_state'].get('color_model'))
        self.assertNotIn('color_temperature', sent_data['desired_state'])

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/light_bulb.json'.format(os.path.dirname(__file__))) as light_file:
            response_dict = json.load(light_file)
        light = response_dict.get('data')[0]
        wink_light = WinkBulb(light, self.api_interface)
        device_id = wink_light.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")

