import json
import unittest
import mock
from pywink import wink_bulb


class LightSetStateTests(unittest.TestCase):

    @mock.patch('requests.put')
    def test_should_send_correct_color_xy_values_to_wink_api(self, put_mock):
        bulb = wink_bulb({})
        color_x = 0.75
        color_y = 0.25
        bulb.setState(True, color_xy=[color_x, color_y])
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals(color_x, sent_data.get('desired_state', {}).get('color_x'))
        self.assertEquals(color_y, sent_data.get('desired_state', {}).get('color_y'))
        self.assertEquals('xy', sent_data['desired_state'].get('color_model'))

    @mock.patch('requests.put')
    def test_should_send_correct_color_temperature_values_to_wink_api(self, put_mock):
        bulb = wink_bulb({})
        arbitrary_kelvin_color = 4950
        bulb.setState(True, color_kelvin=arbitrary_kelvin_color)
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals('color_temperature', sent_data['desired_state'].get('color_model'))
        self.assertEquals(arbitrary_kelvin_color, sent_data['desired_state'].get('color_temperature'))

    @mock.patch('requests.put')
    def test_should_only_send_color_xy_if_both_color_xy_and_color_temperature_are_given(self, put_mock):
        bulb = wink_bulb({})
        arbitrary_kelvin_color = 4950
        bulb.setState(True, color_kelvin=arbitrary_kelvin_color, color_xy=[0, 1])
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals('color_temperature', sent_data['desired_state'].get('color_model'))
        self.assertNotIn('color_x', sent_data['desired_state'])
        self.assertNotIn('color_y', sent_data['desired_state'])
