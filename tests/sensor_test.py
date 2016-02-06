import json
import unittest

from pywink.devices import get_devices_from_response_dict, device_types


class SensorTests(unittest.TestCase):

    def test_quirky_spotter_api_response_should_create_unique_five_sensors(self):
        with open('api_responses/quirky_spotter.json') as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, device_types.SENSOR_POD)
        self.assertEquals(5, len(sensors))
