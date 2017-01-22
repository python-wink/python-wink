import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types


class LockTests(unittest.TestCase):

    def setUp(self):
        super(LockTests, self).setUp()
        self.api_interface = mock.MagicMock()
        device_list = []
        self.response_dict = {}
        _json_file = open('{}/api_responses/schlage_lock.json'.format(os.path.dirname(__file__)))
        device_list.append(json.load(_json_file))
        _json_file.close()
        self.response_dict["data"] = device_list

    def test_lock_state(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertTrue(lock.state())

    def test_lock_alarm_enabled(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertTrue(lock.alarm_enabled())

    def test_lock_alarm_mode(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertEqual(lock.alarm_mode(), "tamper")

    def test_lock_vaction_mode_enabled(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertFalse(lock.vacation_mode_enabled())

    def test_beeper_enabled(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertTrue(lock.beeper_enabled())

    def test_auto_lock_enabled(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertTrue(lock.auto_lock_enabled())

    def test_lock_alarm_sensitivity(self):
        lock = get_devices_from_response_dict(self.response_dict, device_types.LOCK)[0]
        self.assertEqual(lock.alarm_sensitivity(), 0.6)
