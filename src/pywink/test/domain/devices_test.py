import unittest

from pywink.domain.devices import is_desired_state_reached


class IsDesiredStateReachedTests(unittest.TestCase):

    def test_should_return_true_for_bulb_if_desired_brightness_matches_actual_brightness(self):
        brightness = 0.4
        bulb_state = {
            'desired_state': {
                'brightness': brightness
            },
            'brightness': brightness
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_brightness_does_not_match_actual_brightness(self):
        brightness_1 = 0.4
        brightness_2 = 0.5
        bulb_state = {
            'desired_state': {
                'brightness': brightness_1
            },
            'brightness': brightness_2
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_bulb_if_desired_hue_matches_actual_hue(self):
        hue = 0.5
        bulb_state = {
            'desired_state': {
                'hue': hue
            },
            'hue': hue
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_hue_does_not_match_actual_hue(self):
        hue_1 = 0.4
        hue_2 = 0.5
        bulb_state = {
            'desired_state': {
                'hue': hue_1
            },
            'hue': hue_2
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_bulb_if_desired_saturation_matches_actual_saturation(self):
        saturation = 0.5
        bulb_state = {
            'desired_state': {
                'saturation': saturation
            },
            'saturation': saturation
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_saturation_does_not_match_actual_saturation(self):
        saturation_1 = 0.4
        saturation_2 = 0.5
        bulb_state = {
            'desired_state': {
                'saturation': saturation_1
            },
            'saturation': saturation_2
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

    def test_should_return_true_for_bulb_if_desired_powered_matches_actual_powered(self):
        powered = True
        bulb_state = {
            'desired_state': {
                'powered': powered
            },
            'powered': powered
        }
        self.assertTrue(is_desired_state_reached(bulb_state))

    def test_should_return_false_for_bulb_if_desired_powered_does_not_match_actual_powered(self):
        powered_1 = True
        powered_2 = False
        bulb_state = {
            'desired_state': {
                'powered': powered_1
            },
            'powered': powered_2
        }
        self.assertFalse(is_desired_state_reached(bulb_state))

