import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.sensor import WinkSensor
from pywink.devices.piggy_bank import WinkPorkfolioBalanceSensor
from pywink.devices.smoke_detector import WinkSmokeDetector, WinkCoDetector, WinkSmokeSeverity, WinkCoSeverity
from pywink.devices.propane_tank import WinkPropaneTank

class SensorTests(unittest.TestCase):

    def setUp(self):
        super(SensorTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_capability_should_not_be_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.SENSOR_POD)
        for device in devices:
            self.assertIsNotNone(device.capability())

    def test_tamper_detected_should_be_false(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.SENSOR_POD)
        for device in devices:
            self.assertFalse(device.tamper_detected())

    def test_unit_is_valid(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.SENSOR_POD)
        for device in devices:
            if device.unit_type() == "boolean":
                self.assertIsNone(device.unit())
            else:
                self.assertIsNotNone(device.unit())


class EggtrayTests(unittest.TestCase):

    def setUp(self):
        super(EggtrayTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_state_should_be_2(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.EGGTRAY)
        for device in devices:
            self.assertEqual(device.state(), 2)

    def test_capability_is_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.EGGTRAY)
        for device in devices:
            self.assertEqual(device.capability(), None)

    def test_unit_is_eggs(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.EGGTRAY)
        for device in devices:
            self.assertEqual(device.unit(), "eggs")

class KeyTests(unittest.TestCase):

    def setUp(self):
        super(KeyTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_state_should_be_false(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.KEY)
        self.assertEqual(len(devices), 1)
        for device in devices:
            self.assertFalse(device.state())

    def test_parent_id_should_not_be_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.KEY)
        for device in devices:
            self.assertIsNotNone(device.parent_id())

    def test_availble_is_true(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.KEY)
        for device in devices:
            self.assertTrue(device.available())

    def test_capability_is_activity_detected(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.KEY)
        for device in devices:
            self.assertEqual(device.capability(), "activity_detected")

    def test_unit_is_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.KEY)
        for device in devices:
            self.assertIsNone(device.unit())

class PorkfolioTests(unittest.TestCase):

    def setUp(self):
        super(PorkfolioTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_unit_is_usd(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.PIGGY_BANK)
        self.assertEqual(len(devices), 2)
        for device in devices:
            if isinstance(device, WinkPorkfolioBalanceSensor):
                self.assertEqual(device.unit(), "USD")

    def test_capability_is_balance(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.PIGGY_BANK)
        for device in devices:
            if isinstance(device, WinkPorkfolioBalanceSensor):
                self.assertEqual(device.capability(), "balance")

    def test_state_is_180(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.PIGGY_BANK)
        for device in devices:
            if isinstance(device, WinkPorkfolioBalanceSensor):
                self.assertEqual(device.state(), 180)

    def test_available_is_true(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.PIGGY_BANK)
        for device in devices:
            if isinstance(device, WinkPorkfolioBalanceSensor):
                self.assertTrue(device.available())

class GangTests(unittest.TestCase):

    def setUp(self):
        super(GangTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_unit_is_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.GANG)
        for device in devices:
            self.assertIsNone(device.unit())

class SmokeDetectorTests(unittest.TestCase):

    def setUp(self):
        super(SmokeDetectorTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_test_activated_is_false(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.SMOKE_DETECTOR)
        for device in devices:
            self.assertFalse(device.test_activated())

    def test_unit_is_none(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.SMOKE_DETECTOR)
        for device in devices:
            if isinstance(device, WinkSmokeDetector):
                self.assertIsNone(device.unit())
                self.assertEqual(device.unit_type(), "boolean")
            if isinstance(device, WinkCoDetector):
                self.assertIsNone(device.unit())
                self.assertEqual(device.unit_type(), "boolean")
            if isinstance(device, WinkSmokeSeverity):
                self.assertIsNone(device.unit())
                self.assertIsNone(device.unit_type())
            if isinstance(device, WinkCoSeverity):
                self.assertIsNone(device.unit())
                self.assertIsNone(device.unit_type())


class RemoteTests(unittest.TestCase):

    def setUp(self):
        super(RemoteTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_buttons_press_is_false(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.REMOTE)
        remote = devices[0]
        self.assertFalse(remote.button_on_pressed())
        self.assertFalse(remote.button_off_pressed())
        self.assertFalse(remote.button_up_pressed())
        self.assertFalse(remote.button_down_pressed())

    def test_unit_and_capability(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.REMOTE)
        remote = devices[0]
        self.assertIsNone(remote.unit())
        self.assertEqual(remote.capability(), "opened")


class PropaneTankTests(unittest.TestCase):

    def setUp(self):
        super(PropaneTankTests, self).setUp()
        self.api_interface = mock.MagicMock()
        all_devices = os.listdir('{}/api_responses/'.format(os.path.dirname(__file__)))
        self.response_dict = {}
        device_list = []
        for json_file in all_devices:
            if os.path.isfile('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file)):
                _json_file = open('{}/api_responses/{}'.format(os.path.dirname(__file__), json_file))
                device_list.append(json.load(_json_file))
                _json_file.close()
        self.response_dict["data"] = device_list

    def test_unit_and_capability(self):
        devices = get_devices_from_response_dict(self.response_dict, device_types.PROPANE_TANK)
        tank = devices[0]
        self.assertIsNone(tank.unit())
        self.assertIsNone(tank.capability())
