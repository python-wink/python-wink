import json
import mock
import unittest

from pywink import WinkBulb, get_devices_from_response_dict, WinkGarageDoor, WinkPowerStripOutlet, WinkLock, \
    WinkBinarySwitch, WinkSensorPod, WinkEggTray


class LightSetStateTests(unittest.TestCase):

    @mock.patch('requests.put')
    def test_should_send_correct_color_xy_values_to_wink_api(self, put_mock):
        bulb = WinkBulb({})
        color_x = 0.75
        color_y = 0.25
        bulb.set_state(True, color_xy=[color_x, color_y])
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals(color_x, sent_data.get('desired_state', {}).get('color_x'))
        self.assertEquals(color_y, sent_data.get('desired_state', {}).get('color_y'))
        self.assertEquals('xy', sent_data['desired_state'].get('color_model'))

    @mock.patch('requests.put')
    def test_should_send_correct_color_temperature_values_to_wink_api(self, put_mock):
        bulb = WinkBulb({})
        arbitrary_kelvin_color = 4950
        bulb.set_state(True, color_kelvin=arbitrary_kelvin_color)
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals('color_temperature', sent_data['desired_state'].get('color_model'))
        self.assertEquals(arbitrary_kelvin_color, sent_data['desired_state'].get('color_temperature'))

    @mock.patch('requests.put')
    def test_should_only_send_color_xy_if_both_color_xy_and_color_temperature_are_given(self, put_mock):
        bulb = WinkBulb({})
        arbitrary_kelvin_color = 4950
        bulb.set_state(True, color_kelvin=arbitrary_kelvin_color, color_xy=[0, 1])
        sent_data = json.loads(put_mock.call_args[1].get('data'))
        self.assertEquals('color_temperature', sent_data['desired_state'].get('color_model'))
        self.assertNotIn('color_x', sent_data['desired_state'])
        self.assertNotIn('color_y', sent_data['desired_state'])


class WinkAPIResponseHandlingTests(unittest.TestCase):

    def test_should_handle_light_bulb_response(self):
        response = """
        {
            "data": [{
                "light_bulb_id": "33990",
                "name": "downstaurs lamp",
                "locale": "en_us",
                "units": {},
                "created_at": 1410925804,
                "hidden_at": null,
                "capabilities": {},
                "subscription": {},
                "triggers": [],
                "desired_state": {
                    "powered": true,
                    "brightness": 1
                },
                "manufacturer_device_model": "lutron_p_pkg1_w_wh_d",
                "manufacturer_device_id": null,
                "device_manufacturer": "lutron",
                "model_name": "Caseta Wireless Dimmer & Pico",
                "upc_id": "3",
                "hub_id": "11780",
                "local_id": "8",
                "radio_type": "lutron",
                "linked_service_id": null,
                "last_reading": {
                    "brightness": 1,
                    "brightness_updated_at": 1417823487.490747,
                    "connection": true,
                    "connection_updated_at": 1417823487.4907365,
                    "powered": true,
                    "powered_updated_at": 1417823487.4907532,
                    "desired_powered": true,
                    "desired_powered_updated_at": 1417823485.054675,
                    "desired_brightness": 1,
                    "desired_brightness_updated_at": 1417409293.2591703
                },
                "lat_lng": [38.429962, -122.653715],
                "location": "",
                "order": 0
            }]
        }
        """
        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkBulb)

    def test_should_handle_garage_door_opener_response(self):

        response = """
        {
            "data": [{
                "desired_state": {
                    "position": 0
                },
                "last_reading": {
                    "position_opened": "N\/A",
                    "position_opened_updated_at": 1450357467.371,
                    "tamper_detected_true": null,
                    "tamper_detected_true_updated_at": null,
                    "connection": true,
                    "connection_updated_at": 1450357538.2715,
                    "position": 0,
                    "position_updated_at": 1450357537.836,
                    "battery": null,
                    "battery_updated_at": null,
                    "fault": false,
                    "fault_updated_at": 1447976866.0784,
                    "disabled": null,
                    "disabled_updated_at": null,
                    "control_enabled": true,
                    "control_enabled_updated_at": 1447976866.0784,
                    "desired_position_updated_at": 1447976846.8869,
                    "connection_changed_at": 1444775470.5484,
                    "position_changed_at": 1450357537.836,
                    "control_enabled_changed_at": 1444775472.2474,
                    "fault_changed_at": 1444775472.2474,
                    "position_opened_changed_at": 1450357467.371,
                    "desired_position_changed_at": 1447976846.8869
                },
                "garage_door_id": "30528",
                "name": "Garage Door",
                "locale": "en_us",
                "units": {

                },
                "created_at": 1444775470,
                "hidden_at": null,
                "capabilities": {
                    "home_security_device": true
                },
                "triggers": [

                ],
                "manufacturer_device_model": "chamberlain_garage_door_opener",
                "manufacturer_device_id": "1133930",
                "device_manufacturer": "chamberlain",
                "model_name": "MyQ Garage Door Controller",
                "upc_id": "26",
                "upc_code": "012381109302",
                "hub_id": null,
                "local_id": null,
                "radio_type": null,
                "linked_service_id": "206203",
                "lat_lng": [
                    0,
                    0
                ],
                "location": "",
                "order": null
            }],
            "errors": [],
            "pagination": {}
        }
        """
        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkGarageDoor)

    def test_should_handle_power_strip_response(self):

        response = """
        {
            "errors": [

            ],
            "data": [{
                "powerstrip_id": "12345",
                "model_name": "Pivot Power Genius",
                "created_at": 1451578768,
                "mac_address": "0c2a69000000",
                "locale": "en_us",
                "name": "Power strip",
                "units": {

                },
                "last_reading": {
                    "connection": true,
                    "connection_changed_at": 1451947138.418391,
                    "connection_updated_at": 1452093346.488989
                },
                "triggers": [

                ],
                "location": "",
                "capabilities": {

                },
                "hidden_at": null,
                "outlets": [{
                    "parent_object_type": "powerstrip",
                    "icon_id": "4",
                    "desired_state": {
                        "powered": false
                    },
                    "parent_object_id": "24313",
                    "scheduled_outlet_states": [

                    ],
                    "name": "Outlet #1",
                    "outlet_index": 0,
                    "last_reading": {
                        "desired_powered_updated_at": 1452094688.1679382,
                        "powered_updated_at": 1452094688.1461067,
                        "powered": false,
                        "powered_changed_at": 1452094688.1461067
                    },
                    "powered": false,
                    "outlet_id": "48628"
                }, {
                    "parent_object_type": "powerstrip",
                    "icon_id": "4",
                    "desired_state": {
                        "powered": false
                    },
                    "parent_object_id": "24313",
                    "scheduled_outlet_states": [

                    ],
                    "name": "Outlet #2",
                    "outlet_index": 1,
                    "last_reading": {
                        "desired_powered_updated_at": 1452094689.7589157,
                        "powered_updated_at": 1452094689.443459,
                        "powered": false,
                        "powered_changed_at": 1452094689.443459
                    },
                    "powered": false,
                    "outlet_id": "48629"
                }],
                "serial": "AAAA00012345",
                "lat_lng": [
                    0.000000, -0.000000
                ],
                "desired_state": {

                },
                "device_manufacturer": "quirky_ge",
                "upc_id": "24",
                "upc_code": "814434017226"
            }],
            "pagination": {

            }
        }
        """
        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(2, len(devices))
        self.assertIsInstance(devices[0], WinkPowerStripOutlet)
        self.assertIsInstance(devices[1], WinkPowerStripOutlet)

    def test_should_handle_lock_response(self):

        response = """
        {
          "data": [
            {
              "desired_state": {
                "locked": true,
                "beeper_enabled": true,
                "vacation_mode_enabled": false,
                "auto_lock_enabled": false,
                "key_code_length": 4,
                "alarm_mode": null,
                "alarm_sensitivity": 0.6,
                "alarm_enabled": false
              },
              "last_reading": {
                "locked": true,
                "locked_updated_at": 1417823487.490747,
                "connection": true,
                "connection_updated_at": 1417823487.490747,
                "battery": 0.83,
                "battery_updated_at": 1417823487.490747,
                "alarm_activated": null,
                "alarm_activated_updated_at": null,
                "beeper_enabled": true,
                "beeper_enabled_updated_at": 1417823487.490747,
                "vacation_mode_enabled": false,
                "vacation_mode_enabled_updated_at": 1417823487.490747,
                "auto_lock_enabled": false,
                "auto_lock_enabled_updated_at": 1417823487.490747,
                "key_code_length": 4,
                "key_code_length_updated_at": 1417823487.490747,
                "alarm_mode": null,
                "alarm_mode_updated_at": 1417823487.490747,
                "alarm_sensitivity": 0.6,
                "alarm_sensitivity_updated_at": 1417823487.490747,
                "alarm_enabled": true,
                "alarm_enabled_updated_at": 1417823487.490747,
                "last_error": null,
                "last_error_updated_at": 1417823487.490747,
                "desired_locked_updated_at": 1417823487.490747,
                "desired_beeper_enabled_updated_at": 1417823487.490747,
                "desired_vacation_mode_enabled_updated_at": 1417823487.490747,
                "desired_auto_lock_enabled_updated_at": 1417823487.490747,
                "desired_key_code_length_updated_at": 1417823487.490747,
                "desired_alarm_mode_updated_at": 1417823487.490747,
                "desired_alarm_sensitivity_updated_at": 1417823487.490747,
                "desired_alarm_enabled_updated_at": 1417823487.490747,
                "locked_changed_at": 1417823487.490747,
                "battery_changed_at": 1417823487.490747,
                "desired_locked_changed_at": 1417823487.490747,
                "desired_beeper_enabled_changed_at": 1417823487.490747,
                "desired_vacation_mode_enabled_changed_at": 1417823487.490747,
                "desired_auto_lock_enabled_changed_at": 1417823487.490747,
                "desired_key_code_length_changed_at": 1417823487.490747,
                "desired_alarm_mode_changed_at": 1417823487.490747,
                "desired_alarm_sensitivity_changed_at": 1417823487.490747,
                "desired_alarm_enabled_changed_at": 1417823487.490747,
                "last_error_changed_at": 1417823487.490747
              },
              "lock_id": "5304",
              "name": "Main",
              "locale": "en_us",
              "units": {},
              "created_at": 1417823382,
              "hidden_at": null,
              "capabilities": {
                "fields": [
                  {
                    "field": "locked",
                    "type": "boolean",
                    "mutability": "read-write"
                  },
                  {
                    "field": "connection",
                    "mutability": "read-only",
                    "type": "boolean"
                  },
                  {
                    "field": "battery",
                    "mutability": "read-only",
                    "type": "percentage"
                  },
                  {
                    "field": "alarm_activated",
                    "mutability": "read-only",
                    "type": "boolean"
                  },
                  {
                    "field": "beeper_enabled",
                    "type": "boolean"
                  },
                  {
                    "field": "vacation_mode_enabled",
                    "type": "boolean"
                  },
                  {
                    "field": "auto_lock_enabled",
                    "type": "boolean"
                  },
                  {
                    "field": "key_code_length",
                    "type": "integer"
                  },
                  {
                    "field": "alarm_mode",
                    "type": "string"
                  },
                  {
                    "field": "alarm_sensitivity",
                    "type": "percentage"
                  },
                  {
                    "field": "alarm_enabled",
                    "type": "boolean"
                  }
                ],
                "home_security_device": true
              },
              "triggers": [],
              "manufacturer_device_model": "schlage_zwave_lock",
              "manufacturer_device_id": null,
              "device_manufacturer": "schlage",
              "model_name": "BE469",
              "upc_id": "11",
              "upc_code": "043156312214",
              "hub_id": "11780",
              "local_id": "1",
              "radio_type": "zwave",
              "lat_lng": [38.429962, -122.653715],
              "location": ""
            }
          ],
          "errors": [],
          "pagination": {
            "count": 1
          }
        }
        """

        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkLock)

    def test_should_handle_binary_switch_response(self):

        response = """
        {
            "data": [{
                "binary_switch_id": "4153",
                "name": "Garage door indicator",
                "locale": "en_us",
                "units": {},
                "created_at": 1411614982,
                "hidden_at": null,
                "capabilities": {},
                "subscription": {},
                "triggers": [],
                "desired_state": {
                    "powered": false
                },
                "manufacturer_device_model": "leviton_dzs15",
                "manufacturer_device_id": null,
                "device_manufacturer": "leviton",
                "model_name": "Switch",
                "upc_id": "94",
                "gang_id": null,
                "hub_id": "11780",
                "local_id": "9",
                "radio_type": "zwave",
                "last_reading": {
                    "powered": false,
                    "powered_updated_at": 1411614983.6153464,
                    "powering_mode": null,
                    "powering_mode_updated_at": null,
                    "consumption": null,
                    "consumption_updated_at": null,
                    "cost": null,
                    "cost_updated_at": null,
                    "budget_percentage": null,
                    "budget_percentage_updated_at": null,
                    "budget_velocity": null,
                    "budget_velocity_updated_at": null,
                    "summation_delivered": null,
                    "summation_delivered_updated_at": null,
                    "sum_delivered_multiplier": null,
                    "sum_delivered_multiplier_updated_at": null,
                    "sum_delivered_divisor": null,
                    "sum_delivered_divisor_updated_at": null,
                    "sum_delivered_formatting": null,
                    "sum_delivered_formatting_updated_at": null,
                    "sum_unit_of_measure": null,
                    "sum_unit_of_measure_updated_at": null,
                    "desired_powered": false,
                    "desired_powered_updated_at": 1417893563.7567682,
                    "desired_powering_mode": null,
                    "desired_powering_mode_updated_at": null
                },
                "current_budget": null,
                "lat_lng": [
                    38.429996,
                    -122.653721
                ],
                "location": "",
                "order": 0
            }],
            "errors": [],
            "pagination": {}
        }
        """

        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkBinarySwitch)

    def test_should_handle_sensor_pod_response(self):

        response = """
        {
            "data": [{
                "last_event": {
                    "brightness_occurred_at": null,
                    "loudness_occurred_at": null,
                    "vibration_occurred_at": null
                },
                "model_name": "Tripper",
                "capabilities": {
                    "sensor_types": [
                        {
                            "field": "opened",
                            "type": "boolean"
                        },
                        {
                            "field": "battery",
                            "type": "percentage"
                        }
                    ]
                },
                "manufacturer_device_model": "quirky_ge_tripper",
                "location": "",
                "radio_type": "zigbee",
                "manufacturer_device_id": null,
                "gang_id": null,
                "sensor_pod_id": "37614",
                "subscription": {
                },
                "units": {
                },
                "upc_id": "184",
                "hidden_at": null,
                "last_reading": {
                    "battery_voltage_threshold_2": 0,
                    "opened": false,
                    "battery_alarm_mask": 0,
                    "opened_updated_at": 1421697092.7347496,
                    "battery_voltage_min_threshold_updated_at": 1421697092.7347229,
                    "battery_voltage_min_threshold": 0,
                    "connection": null,
                    "battery_voltage": 25,
                    "battery_voltage_threshold_1": 25,
                    "connection_updated_at": null,
                    "battery_voltage_threshold_3": 0,
                    "battery_voltage_updated_at": 1421697092.7347066,
                    "battery_voltage_threshold_1_updated_at": 1421697092.7347302,
                    "battery_voltage_threshold_3_updated_at": 1421697092.7347434,
                    "battery_voltage_threshold_2_updated_at": 1421697092.7347374,
                    "battery": 1.0,
                    "battery_updated_at": 1421697092.7347553,
                    "battery_alarm_mask_updated_at": 1421697092.734716
                },
                "triggers": [
                ],
                "name": "MasterBathroom",
                "lat_lng": [
                    37.550773,
                    -122.279182
                ],
                "uuid": "a2cb868a-dda3-4211-ab73-fc08087aeed7",
                "locale": "en_us",
                "device_manufacturer": "quirky_ge",
                "created_at": 1421523277,
                "local_id": "2",
                "hub_id": "88264"
            }]
        }
        """

        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkSensorPod)

    def test_should_handle_egg_tray_response(self):

        response = """
        {
            "data": [{
                "last_reading": {
                    "connection": true,
                    "connection_updated_at": 1417823487.490747,
                    "battery": 0.83,
                    "battery_updated_at": 1417823487.490747,
                    "inventory": 3,
                    "inventory_updated_at": 1449705551.7313306,
                    "freshness_remaining": 2419191,
                    "freshness_remaining_updated_at": 1449705551.7313495,
                    "age_updated_at": 1449705551.7313418,
                    "age": 1449705542,
                    "connection_changed_at": 1449705443.6858568,
                    "next_trigger_at_updated_at": null,
                    "next_trigger_at": null,
                    "egg_1_timestamp_updated_at": 1449753143.8631344,
                    "egg_1_timestamp_changed_at": 1449705534.0782206,
                    "egg_1_timestamp": 1449705545.0,
                    "egg_2_timestamp_updated_at": 1449753143.8631344,
                    "egg_2_timestamp_changed_at": 1449705534.0782206,
                    "egg_2_timestamp": 1449705545.0,
                    "egg_3_timestamp_updated_at": 1449753143.8631344,
                    "egg_3_timestamp_changed_at": 1449705534.0782206,
                    "egg_3_timestamp": 1449705545.0,
                    "egg_4_timestamp_updated_at": 1449753143.8631344,
                    "egg_4_timestamp_changed_at": 1449705534.0782206,
                    "egg_4_timestamp": 1449705545.0,
                    "egg_5_timestamp_updated_at": 1449753143.8631344,
                    "egg_5_timestamp_changed_at": 1449705534.0782206,
                    "egg_5_timestamp": 1449705545.0,
                    "egg_6_timestamp_updated_at": 1449753143.8631344,
                    "egg_6_timestamp_changed_at": 1449705534.0782206,
                    "egg_6_timestamp": 1449705545.0,
                    "egg_7_timestamp_updated_at": 1449753143.8631344,
                    "egg_7_timestamp_changed_at": 1449705534.0782206,
                    "egg_7_timestamp": 1449705545.0,
                    "egg_8_timestamp_updated_at": 1449753143.8631344,
                    "egg_8_timestamp_changed_at": 1449705534.0782206,
                    "egg_8_timestamp": 1449705545.0,
                    "egg_9_timestamp_updated_at": 1449753143.8631344,
                    "egg_9_timestamp_changed_at": 1449705534.0782206,
                    "egg_9_timestamp": 1449705545.0,
                    "egg_10_timestamp_updated_at": 1449753143.8631344,
                    "egg_10_timestamp_changed_at": 1449705534.0782206,
                    "egg_10_timestamp": 1449705545.0,
                    "egg_11_timestamp_updated_at": 1449753143.8631344,
                    "egg_11_timestamp_changed_at": 1449705534.0782206,
                    "egg_11_timestamp": 1449705545.0,
                    "egg_12_timestamp_updated_at": 1449753143.8631344,
                    "egg_12_timestamp_changed_at": 1449705534.0782206,
                    "egg_12_timestamp": 1449705545.0,
                    "egg_13_timestamp_updated_at": 1449753143.8631344,
                    "egg_13_timestamp_changed_at": 1449705534.0782206,
                    "egg_13_timestamp": 1449705545.0,
                    "egg_14_timestamp_updated_at": 1449753143.8631344,
                    "egg_14_timestamp_changed_at": 1449705534.0782206,
                    "egg_14_timestamp": 1449705545.0
                },
                "eggtray_id": "153869",
                "name": "Egg Minder",
                "freshness_period": 2419200,
                "locale": "en_us",
                "units": {},
                "created_at": 1417823382,
                "hidden_at": null,
                "capabilities": {},
                "triggers": [],
                "device_manufacturer": "quirky_ge",
                "model_name": "Egg Minder",
                "upc_id": "23",
                "upc_code": "814434017233",
                "lat_lng": [38.429962, -122.653715],
                "location": ""
            }],
            "errors": [],
            "pagination": {
                "count": 1
            }
        }
        """

        response_dict = json.loads(response)
        devices = get_devices_from_response_dict(response_dict)
        self.assertEqual(1, len(devices))
        self.assertIsInstance(devices[0], WinkEggTray)
