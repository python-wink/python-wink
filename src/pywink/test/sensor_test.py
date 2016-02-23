import json
import os
import unittest

from pywink.devices import types as device_types
from pywink.api import get_devices_from_response_dict
from pywink.devices.sensors import WinkBrightnessSensor, WinkHumiditySensor, WinkSoundPresenceSensor, \
    WinkVibrationPresenceSensor, WinkTemperatureSensor
from pywink.devices.types import DEVICE_ID_KEYS


class SensorTests(unittest.TestCase):

    def test_quirky_spotter_api_response_should_create_unique_one_primary_sensor_and_five_subsensors(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        self.assertEquals(1 + 5, len(sensors))

    def test_alternative_quirky_spotter_api_response_should_create_one_primary_sensor_and_five_subsensors(self):
        with open('{}/api_responses/quirky_spotter_2.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        self.assertEquals(1 + 5, len(sensors))

    def test_brightness_should_have_correct_value(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkBrightnessSensor"""
        brightness_sensor = [sensor for sensor in sensors if sensor.capability() is WinkBrightnessSensor.CAPABILITY][0]
        expected_brightness = 1
        self.assertEquals(expected_brightness, brightness_sensor.brightness_boolean())

    def test_humidity_should_have_correct_value(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkHumiditySensor"""
        humidity_sensor = [sensor for sensor in sensors if sensor.capability() is WinkHumiditySensor.CAPABILITY][0]
        expected_humidity = 48
        self.assertEquals(expected_humidity, humidity_sensor.humidity_percentage())

    def test_loudness_should_have_correct_value(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkSoundPresenceSensor"""
        sound_sensor = [sensor for sensor in sensors if sensor.capability() is WinkSoundPresenceSensor.CAPABILITY][0]
        expected_sound_presence = False
        self.assertEquals(expected_sound_presence, sound_sensor.loudness_boolean())

    def test_vibration_should_have_correct_value(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkVibrationPresenceSensor"""
        sound_sensor = [sensor for sensor in sensors if sensor.capability() is WinkVibrationPresenceSensor.CAPABILITY][0]
        expected_vibrartion_presence = False
        self.assertEquals(expected_vibrartion_presence, sound_sensor.vibration_boolean())

    def test_temperature_should_have_correct_value(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkTemperatureSensor"""
        sound_sensor = [sensor for sensor in sensors if sensor.capability() is WinkTemperatureSensor.CAPABILITY][0]
        expected_temperature = 5
        self.assertEquals(expected_temperature, sound_sensor.temperature_float())
