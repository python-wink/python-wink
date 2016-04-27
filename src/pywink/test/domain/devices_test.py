import unittest

from pywink.domain.devices import is_desired_state_reached
from pywink.test.devices.standard.api_responses import ApiResponseJSONLoader

class IsDesiredStateReachedTests(unittest.TestCase):

    def test_should_return_true_for_bulb_if_desired_brightness_matches_actual_brightness(self):
        brightness = 0.4
        bulb_state = {
            'desired_state': {
                'brightness': brightness
            },
            'last_reading': {
                'brightness': brightness
            }
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_brightness_does_not_match_actual_brightness(self):
        brightness_1 = 0.4
        brightness_2 = 0.5
        bulb_state = {
            'desired_state': {
                'brightness': brightness_1
            },
            'last_reading': {
                'brightness': brightness_2
            }
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_bulb_if_desired_hue_matches_actual_hue(self):
        hue = 0.5
        bulb_state = {
            'desired_state': {
                'hue': hue
            },
            'last_reading': {
                'hue': hue
            }
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_hue_does_not_match_actual_hue(self):
        hue_1 = 0.4
        hue_2 = 0.5
        bulb_state = {
            'desired_state': {
                'hue': hue_1
            },
            'last_reading': {
                'hue': hue_2
            }
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_bulb_if_desired_saturation_matches_actual_saturation(self):
        saturation = 0.5
        bulb_state = {
            'desired_state': {
                'saturation': saturation
            },
            'last_reading': {
                'saturation': saturation
            }
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_saturation_does_not_match_actual_saturation(self):
        saturation_1 = 0.4
        saturation_2 = 0.5
        bulb_state = {
            'desired_state': {
                'saturation': saturation_1
            },
            'last_reading': {
                'saturation': saturation_2
            }
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_bulb_if_desired_powered_matches_actual_powered(self):
        powered = True
        bulb_state = {
            'desired_state': {
                'powered': powered
            },
            'last_reading': {
                'powered': powered
            }
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_powered_does_not_match_actual_powered(self):
        powered_1 = True
        powered_2 = False
        bulb_state = {
            'desired_state': {
                'powered': powered_1
            },
            'last_reading': {
                'powered': powered_2
            }
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_real_state_which_where_desired_state_is_reached(self):
        response_dict = ApiResponseJSONLoader('light_bulb_with_desired_state_reached.json').load()['data']
        self.assertTrue(is_desired_state_reached(response_dict))

    def test_should_return_true_if_device_is_disconnected(self):
        bulb_state = {
            'desired_state': {
                'powered': True
            },
            'last_reading': {
                'connection': False,
                'powered': False
            }
        }
        self.assertTrue(is_desired_state_reached(bulb_state))
