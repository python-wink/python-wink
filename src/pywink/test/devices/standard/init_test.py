import json
import mock
import unittest
import sys
import os

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.sensors import WinkSensorPod, WinkBrightnessSensor, WinkHumiditySensor, \
     WinkSoundPresenceSensor, WinkVibrationPresenceSensor, WinkTemperatureSensor, \
     _WinkCapabilitySensor
from pywink.devices.standard import WinkBulb, WinkGarageDoor, WinkPowerStripOutlet, WinkSiren, WinkLock, \
     WinkShade, WinkBinarySwitch, WinkEggTray
from pywink.devices.types import DEVICE_ID_KEYS


class PowerStripTests(unittest.TestCase):

    def setUp(self):
        super(PowerStripTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_power_strip_response(self):
        with open('{}/api_responses/power_strip.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.POWER_STRIP])
        self.assertEqual(2, len(devices))
        self.assertIsInstance(devices[0], WinkPowerStripOutlet)
        self.assertIsInstance(devices[1], WinkPowerStripOutlet)

    def test_should_show_powered_state_as_false_if_device_is_disconnected(self):
        with open('{}/api_responses/power_strip.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.POWER_STRIP])
        self.assertFalse(devices[0].state())

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/power_strip.json'.format(os.path.dirname(__file__))) as powerstrip_file:
            response_dict = json.load(powerstrip_file)
        power_strip = response_dict.get('data')
        outlets = power_strip[0].get('outlets')

        for outlet in outlets:
            wink_outlet = WinkPowerStripOutlet(outlet, self.api_interface)
            device_id = wink_outlet.device_id()
            self.assertRegex(device_id, "^[0-9]{4,6}$")


class GarageDoorTests(unittest.TestCase):

    def setUp(self):
        super(GarageDoorTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_garage_door_opener_response(self):
        with open('{}/api_responses/garage_door.json'.format(os.path.dirname(__file__))) as garage_door_file:
            response_dict = json.load(garage_door_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.GARAGE_DOOR])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkGarageDoor)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/garage_door.json'.format(os.path.dirname(__file__))) as garage_door_file:
            response_dict = json.load(garage_door_file)
        garage_door = response_dict.get('data')[0]
        wink_garage_door = WinkGarageDoor(garage_door, self.api_interface)
        device_id = wink_garage_door.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class ShadeTests(unittest.TestCase):
    def setUp(self):
        super(ShadeTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_shade_response(self):
        with open('{}/api_responses/shade.json'.format(os.path.dirname(__file__))) as shade_file:
            response_dict = json.load(shade_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SHADE])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkShade)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/shade.json'.format(os.path.dirname(__file__))) as shade_file:
            response_dict = json.load(shade_file)
        print(response_dict)
        shade = response_dict.get('data')[0]
        wink_shade = WinkShade(shade, self.api_interface)
        device_id = wink_shade.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class SirenTests(unittest.TestCase):

    def setUp(self):
        super(SirenTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_siren_response(self):
        with open('{}/api_responses/siren.json'.format(os.path.dirname(__file__))) as siren_file:
            response_dict = json.load(siren_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SIREN])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkSiren)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/siren.json'.format(os.path.dirname(__file__))) as siren_file:
            response_dict = json.load(siren_file)
        siren = response_dict.get('data')[0]
        wink_siren = WinkSiren(siren, self.api_interface)
        device_id = wink_siren.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class LockTests(unittest.TestCase):

    def setUp(self):
        super(LockTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_lock_response(self):
        with open('{}/api_responses/lock.json'.format(os.path.dirname(__file__))) as lock_file:
            response_dict = json.load(lock_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LOCK])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkLock)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/lock.json'.format(os.path.dirname(__file__))) as lock_file:
            response_dict = json.load(lock_file)
        lock = response_dict.get('data')[0]
        wink_lock = WinkLock(lock, self.api_interface)
        device_id = wink_lock.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class BinarySwitchTests(unittest.TestCase):

    def setUp(self):
        super(BinarySwitchTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_binary_switch_response(self):
        with open('{}/api_responses/binary_switch.json'.format(os.path.dirname(__file__))) as binary_switch_file:
            response_dict = json.load(binary_switch_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.BINARY_SWITCH])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkBinarySwitch)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/binary_switch.json'.format(os.path.dirname(__file__))) as binary_switch_file:
            response_dict = json.load(binary_switch_file)
        switch = response_dict.get('data')[0]
        wink_switch = WinkBinarySwitch(switch, self.api_interface)
        device_id = wink_switch.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class BinarySensorTests(unittest.TestCase):

    def setUp(self):
        super(BinarySensorTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_sensor_pod_response(self):
        with open('{}/api_responses/binary_sensor.json'.format(os.path.dirname(__file__))) as binary_sensor_file:
            response_dict = json.load(binary_sensor_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkSensorPod)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/binary_sensor.json'.format(os.path.dirname(__file__))) as binary_sensor_file:
            response_dict = json.load(binary_sensor_file)
        sensor = response_dict.get('data')[0]
        wink_binary_sensor = WinkSensorPod(sensor, self.api_interface)
        device_id = wink_binary_sensor.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class EggtrayTests(unittest.TestCase):

    def setUp(self):
        super(EggtrayTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_handle_egg_tray_response(self):
        with open('{}/api_responses/eggtray.json'.format(os.path.dirname(__file__))) as eggtray_file:
            response_dict = json.load(eggtray_file)
        devices = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.EGG_TRAY])
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkEggTray)

    def test_device_id_should_be_number(self):
        with open('{}/api_responses/eggtray.json'.format(os.path.dirname(__file__))) as eggtray_file:
            response_dict = json.load(eggtray_file)
        eggtray = response_dict.get('data')[0]
        wink_eggtray = WinkEggTray(eggtray, self.api_interface)
        device_id = wink_eggtray.device_id()
        self.assertRegex(device_id, "^[0-9]{4,6}$")


class SensorTests(unittest.TestCase):

    def setUp(self):
        super(SensorTests, self).setUp()
        self.api_interface = mock.MagicMock()

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
        vibration_sensor = [sensor for sensor in sensors if sensor.capability() is WinkVibrationPresenceSensor.CAPABILITY][0]
        expected_vibrartion_presence = False
        self.assertEquals(expected_vibrartion_presence, vibration_sensor.vibration_boolean())

    def test_temperature_should_have_correct_value(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkTemperatureSensor"""
        temp_sensor = [sensor for sensor in sensors if sensor.capability() is WinkTemperatureSensor.CAPABILITY][0]
        expected_temperature = 5
        self.assertEquals(expected_temperature, temp_sensor.temperature_float())

    def test_device_id_should_start_with_a_number(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])

        for sensor in sensors:
            device_id = sensor.device_id()
            self.assertRegex(device_id, "^[0-9]{4,6}")

    def test_battery_level_should_return_none(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])

        for sensor in sensors:
            self.assertIsNone(sensor.battery_level)

    def test_battery_level_should_return_float(self):
        with open('{}/api_responses/quirky_spotter_2.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])

        for sensor in sensors:
            self.assertEqual(sensor.battery_level, 0.86)


    def test_humidity_is_percentage_after_update(self):
        with open('{}/api_responses/quirky_spotter.json'.format(os.path.dirname(__file__))) as spotter_file:
            response_dict = json.load(spotter_file)

        sensors = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.SENSOR_POD])
        """:type : list of WinkHumiditySensor"""
        humidity_sensor = [sensor for sensor in sensors if sensor.capability() is WinkHumiditySensor.CAPABILITY][0]
        
        with open('{}/api_responses/quirky_spotter_pubnub.json'.format(os.path.dirname(__file__))) as spotter_file:
            update_response_dict = json.load(spotter_file)

        humidity_sensor.pubnub_update(update_response_dict)
        expected_humidity = 24
        self.assertEquals(expected_humidity, humidity_sensor.humidity_percentage())

class WinkCapabilitySensorTests(unittest.TestCase):

    def setUp(self):
        super(WinkCapabilitySensorTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_should_call_get_state_endpoint_with_capability_removed_from_id(self):
        expected_id = '72503'
        unit = 'DEG'  # mock doesn't like unicode
        capability = "Test"
        sensor = _WinkCapabilitySensor({
            'sensor_pod_id': expected_id
        }, self.api_interface, unit, capability)

        sensor.update_state()
        self.api_interface.get_device_state.assert_called_once_with(sensor, expected_id)

        
class WinkPubnubTests(unittest.TestCase):

    def setUp(self):
        super(WinkPubnubTests, self).setUp()
        self.api_interface = mock.MagicMock()

    def test_pubnub_key_and_channel_should_not_be_none(self):
        with open('{}/api_responses/device_with_pubnub.json'.format(os.path.dirname(__file__))) as lock_file:
            response_dict = json.load(lock_file)
        device = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LOCK])[0]

        self.assertIsNotNone(device.pubnub_key)
        self.assertIsNotNone(device.pubnub_channel)

    def test_pubnub_key_and_channel_should_be_none(self):
        with open('{}/api_responses/lock.json'.format(os.path.dirname(__file__))) as lock_file:
            response_dict = json.load(lock_file)
        device = get_devices_from_response_dict(response_dict, DEVICE_ID_KEYS[device_types.LOCK])[0]

        self.assertIsNone(device.pubnub_key)
        self.assertIsNone(device.pubnub_channel)

    def test_pywink_api_pubnub_subscription_key_is_not_none(self):
        with open('{}/api_responses/device_with_pubnub.json'.format(os.path.dirname(__file__))) as lock_file:
            response_dict = json.load(lock_file)

        self.assertIsNotNone(self.api_interface.get_subscription_key_from_response_dict(response_dict))
