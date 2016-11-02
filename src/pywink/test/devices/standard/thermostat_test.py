import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.standard import WinkThermostat
from pywink.devices.types import DEVICE_ID_KEYS


class ThermostatModeTests(unittest.TestCase):

    def test_should_be_true_if_thermostat_is_on(self):
        with open('{}/api_responses/nest.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue(thermostat.is_on())

    def test_should_be_true_if_response_contains_heat_capabilities(self):
        with open('{}/api_responses/nest.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('heat_only' in thermostat.hvac_modes())

    def test_should_be_true_if_response_contains_cool_capabilities(self):
        with open('{}/api_responses/nest.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('cool_only' in thermostat.hvac_modes())

    def test_should_be_true_if_response_contains_auto_capabilities(self):
        with open('{}/api_responses/nest.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('auto' in thermostat.hvac_modes())

    def test_should_be_false_if_response_doesnt_contains_aux_capabilities(self):
        with open('{}/api_responses/nest.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertFalse('aux' in thermostat.hvac_modes())

    def test_should_be_cool_only_for_current_hvac_mode(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual('cool_only', thermostat.current_hvac_mode())

class ThermostatFanTests(unittest.TestCase):

    def test_should_be_true_if_response_contains_fan_on_capabilities(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('on' in thermostat.fan_modes())

    def test_should_be_true_if_response_contains_fan_auto_capabilities(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('auto' in thermostat.fan_modes())

    def test_should_be_true_if_response_contains_fan_on_capabilities(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('auto' in thermostat.fan_modes())

    def test_should_be_true_if_thermostat_fan_is_on(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue(thermostat.fan_on())

    def test_should_be_true_if_thermostat_has_fan(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue(thermostat.has_fan())

    def test_should_be_auto_for_current_fan_mode(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual('auto', thermostat.current_fan_mode())


class ThermostatAvailableOptionsTests(unittest.TestCase):

    def test_should_be_true_if_thermostat_has_detected_occupancy(self):
        # sensi.json been faked to add in the occupied field for testing.
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue(thermostat.occupied())

    def test_should_be_true_if_thermostat_set_to_eco_mode(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertFalse(thermostat.eco_target())

    def test_should_be_true_if_thermostat_set_to_away(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertFalse(thermostat.away())

    def test_current_units_should_be_f(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual('f', thermostat.current_units())

class ThermostatTemperatureTests(unittest.TestCase):

    def test_set_point_limits(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(7.222222222222222, thermostat.min_min_set_point())
        self.assertEqual(7.222222222222222, thermostat.min_max_set_point())
        self.assertEqual(37.22222222222222, thermostat.max_min_set_point())
        self.assertEqual(37.22222222222222, thermostat.max_max_set_point())

    def test_deadband(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(1.1111111111111112, thermostat.deadband())

    def test_current_external_temp(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(16.1, thermostat.current_external_temperature())

    def test_current_temp(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(20.555555555555557, thermostat.current_temperature())

    def test_current_max_set_point(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(22.22222222222222, thermostat.current_max_set_point())

    def test_current_min_set_point(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(22.22222222222222, thermostat.current_min_set_point())

    def test_current_smart_temperature(self):
        # This result is only present on ecobee thermostats, the sensi.json has
        # been faked to add in the smart_temperature field for testing.
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(20.555555555555557, thermostat.current_smart_temperature())


class ThermostatHumidityTests(unittest.TestCase):

    def test_current_humidity(self):
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(40, thermostat.current_humidity())

    def test_current_humidifier_mode(self):
        # sensi.json been faked to add in the humidifier_mode field for testing.
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual('auto', thermostat.current_humidifier_mode())

    def test_current_dehumidifier_mode(self):
        # sensi.json been faked to add in the dehumidifier_mode field
        # for testing.
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual('auto', thermostat.current_dehumidifier_mode())

    def test_current_humidifier_set_point(self):
        # sensi.json has been faked to add in the humidifier_set_point
        # field for testing.
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(0.2, thermostat.current_humidifier_set_point())

    def test_current_dehumidifier_set_point(self):
        # sensi.json has been faked to add in the dehumidifier_set_point
        # field for testing.
        with open('{}/api_responses/sensi.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertEqual(0.6, thermostat.current_dehumidifier_set_point())

class GenericZwaveThermostatTests(unittest.TestCase):

    def test_should_be_true_if_response_contains_aux_capabilities(self):
        with open('{}/api_responses/gocontrol_thermostat.json'.format(os.path.dirname(__file__))) as thermostat_file:
            response_dict = json.load(thermostat_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.THERMOSTAT])

        thermostat = devices[0]
        """ :type thermostat: pywink.devices.standard.WinkThermostat """
        self.assertTrue('aux' in thermostat.hvac_modes())
