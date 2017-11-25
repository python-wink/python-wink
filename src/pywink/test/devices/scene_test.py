import json
import os
import unittest

from pywink.api import get_devices_from_response_dict
from pywink.devices import types as device_types


class SceneTests(unittest.TestCase):

    def test_state_should_be_false(self):
        with open('{}/api_responses/scene.json'.format(os.path.dirname(__file__))) as scene_file:
            response_dict = json.load(scene_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.SCENE)

        scene = devices[0]
        self.assertFalse(scene.state())

    def test_available_should_be_true(self):
        with open('{}/api_responses/scene.json'.format(os.path.dirname(__file__))) as scene_file:
            response_dict = json.load(scene_file)
        response_dict = {"data": [response_dict]}
        devices = get_devices_from_response_dict(response_dict, device_types.SCENE)

        scene = devices[0]
        self.assertTrue(scene.available())
