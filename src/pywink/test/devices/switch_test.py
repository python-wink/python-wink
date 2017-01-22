import json
import os
import unittest

import mock

from pywink.api import get_devices_from_response_dict, WinkApiInterface
from pywink.devices import types as device_types
from pywink.devices.binary_switch import WinkBinarySwitch


class BinarySwitchTests(unittest.TestCase):

    def test_state_should_be_false(self):
        with open('{}/api_responses/ge_zwave_switch.json'.format(os.path.dirname(__file__))) as binary_switch_file:
            response_dict = json.load(binary_switch_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.BINARY_SWITCH)

        switch = devices[0]
        self.assertFalse(switch.state())
