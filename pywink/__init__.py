"""
Objects for interfacing with the Wink API
"""
import logging
import json
import time
import requests

BASE_URL = "https://winkapi.quirky.com"

HEADERS = {}


class WinkDevice(object):
    @staticmethod
    def factory(device_state_as_json):

        new_object = None

        # pylint: disable=redefined-variable-type
        # These objects all share the same base class: WinkDevice

        if "light_bulb_id" in device_state_as_json:
            new_object = WinkBulb(device_state_as_json)
        elif "sensor_pod_id" in device_state_as_json:
            new_object = WinkSensorPod(device_state_as_json)
        elif "binary_switch_id" in device_state_as_json:
            new_object = WinkBinarySwitch(device_state_as_json)
        elif "outlet_id" in device_state_as_json:
            new_object = WinkPowerStripOutlet(device_state_as_json)
        elif "lock_id" in device_state_as_json:
            new_object = WinkLock(device_state_as_json)
        elif "eggtray_id" in device_state_as_json:
            new_object = WinkEggTray(device_state_as_json)
        elif "garage_door_id" in device_state_as_json:
            new_object = WinkGarageDoor(device_state_as_json)

        return new_object or WinkDevice(device_state_as_json)

    def __init__(self, device_state_as_json, objectprefix=None):
        self.objectprefix = objectprefix
        self.json_state = device_state_as_json

    def __str__(self):
        return "%s %s %s" % (self.name(), self.device_id(), self.state())

    def __repr__(self):
        return "<Wink object %s %s %s>" \
               % (self.name(), self.device_id(), self.state())

    def name(self):
        return self.json_state.get('name', "Unknown Name")

    def state(self):
        raise NotImplementedError("Must implement state")

    def device_id(self):
        raise NotImplementedError("Must implement device_id")

    @property
    def _last_reading(self):
        return self.json_state.get('last_reading') or {}

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        self.json_state = response_json.get('data')

    def update_state(self):
        """ Update state with latest info from Wink API. """
        url_string = "{}/{}/{}".format(BASE_URL,
                                       self.objectprefix, self.device_id())
        arequest = requests.get(url_string, headers=HEADERS)
        self._update_state_from_response(arequest.json())

    def refresh_state_at_hub(self):
        """
        Tell hub to query latest status from device and upload to Wink.
        PS: Not sure if this even works..
        """
        url_string = "{}/{}/{}/refresh".format(BASE_URL,
                                               self.objectprefix,
                                               self.device_id())
        requests.get(url_string, headers=HEADERS)


class WinkEggTray(WinkDevice):
    """ represents a wink.py egg tray
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:
{
    "data": {
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
            "next_trigger_at_updated_at": None,
            "next_trigger_at": None,
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
            "egg_14_timestamp": 1449705545.0,
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
        },
  "errors": [],
  "pagination": {
    "count": 1
  }
}

"""

    def __init__(self, device_state_as_json, objectprefix="eggtrays"):
        super(WinkEggTray, self).__init__(device_state_as_json,
                                          objectprefix=objectprefix)

    def __repr__(self):
        return "<Wink eggtray Name:%s" \
               " Device_id:%s state:%s>" % (self.name(),
                                            self.device_id(), self.state())

    def state(self):
        if 'inventory' in self._last_reading:
            return self._last_reading['inventory']
        return False

    def device_id(self):
        return self.json_state.get('eggtray_id', self.name())


class WinkSensorPod(WinkDevice):
    """ represents a wink.py sensor
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:
{
    "data": {
        "last_event": {
            "brightness_occurred_at": None,
            "loudness_occurred_at": None,
            "vibration_occurred_at": None
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
        "manufacturer_device_id": None,
        "gang_id": None,
        "sensor_pod_id": "37614",
        "subscription": {
        },
        "units": {
        },
        "upc_id": "184",
        "hidden_at": None,
        "last_reading": {
            "battery_voltage_threshold_2": 0,
            "opened": False,
            "battery_alarm_mask": 0,
            "opened_updated_at": 1421697092.7347496,
            "battery_voltage_min_threshold_updated_at": 1421697092.7347229,
            "battery_voltage_min_threshold": 0,
            "connection": None,
            "battery_voltage": 25,
            "battery_voltage_threshold_1": 25,
            "connection_updated_at": None,
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
    },
}

     """

    def __init__(self, device_state_as_json, objectprefix="sensor_pods"):
        super(WinkSensorPod, self).__init__(device_state_as_json,
                                            objectprefix=objectprefix)

    def __repr__(self):
        return "<Wink sensor %s %s %s>" % (self.name(),
                                           self.device_id(), self.state())

    def state(self):
        if 'opened' in self._last_reading:
            return self._last_reading['opened']
        elif 'motion' in self._last_reading:
            return self._last_reading['motion']
        return False

    def device_id(self):
        return self.json_state.get('sensor_pod_id', self.name())


class WinkBinarySwitch(WinkDevice):
    """ represents a wink.py switch
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:

{
    "data": {
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
    },
    "errors": [],
    "pagination": {}
}

     """

    def __init__(self, device_state_as_json, objectprefix="binary_switches"):
        super(WinkBinarySwitch, self).__init__(device_state_as_json,
                                               objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink switch %s %s %s>" % (self.name(),
                                           self.device_id(), self.state())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('powered', False)

    def device_id(self):
        return self.json_state.get('binary_switch_id', self.name())

    # pylint: disable=unused-argument
    # kwargs is unused here but is used by child implementations
    def set_state(self, state, **kwargs):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        url_string = "{}/{}/{}".format(BASE_URL,
                                       self.objectprefix, self.device_id())
        values = {"desired_state": {"powered": state}}
        arequest = requests.put(url_string,
                                data=json.dumps(values), headers=HEADERS)
        self._update_state_from_response(arequest.json())

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_powered') == last_read.get('powered') \
                    or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkBulb(WinkBinarySwitch):
    """ represents a wink.py bulb
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:

     "light_bulb_id": "33990",
    "name": "downstaurs lamp",
    "locale": "en_us",
    "units":{},
    "created_at": 1410925804,
    "hidden_at": null,
    "capabilities":{},
    "subscription":{},
    "triggers":[],
    "desired_state":{"powered": true, "brightness": 1},
    "manufacturer_device_model": "lutron_p_pkg1_w_wh_d",
    "manufacturer_device_id": null,
    "device_manufacturer": "lutron",
    "model_name": "Caseta Wireless Dimmer & Pico",
    "upc_id": "3",
    "hub_id": "11780",
    "local_id": "8",
    "radio_type": "lutron",
    "linked_service_id": null,
    "last_reading":{
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
    "lat_lng":[38.429962, -122.653715],
    "location": "",
    "order": 0

     """
    json_state = {}

    def __init__(self, device_state_as_json):
        super().__init__(device_state_as_json,
                         objectprefix="light_bulbs")

    def device_id(self):
        return self.json_state.get('light_bulb_id', self.name())

    def brightness(self):
        return self._last_reading.get('brightness')

    def color_xy(self):
        """
        XY colour value: [float, float] or None
        :rtype: list float
        """
        color_x = self._last_reading.get('color_x')
        color_y = self._last_reading.get('color_y')

        if color_x and color_y:
            return [float(color_x), float(color_y)]

        return None

    def color_temperature_kelvin(self):
        """
        Color temperature, in degrees Kelvin.
        Eg: "Daylight" light bulbs are 4600K
        :rtype: int
        """
        return self._last_reading.get('color_temperature')

    def set_state(self, state, brightness=None,
                  color_kelvin=None, color_xy=None, **kwargs):
        """
        :param state:   a boolean of true (on) or false ('off')
        :param brightness: a float from 0 to 1 to set the brightness of
         this bulb
        :param color_kelvin: an integer greater than 0 which is a color in
         degrees Kelvin
        :param color_xy: a pair of floats in a list which specify the desired
         CIE 1931 x,y color coordinates
        :return: nothing
        """
        url_string = "{}/light_bulbs/{}".format(BASE_URL, self.device_id())
        values = {
            "desired_state": {
                "powered": state
            }
        }

        if brightness is not None:
            values["desired_state"]["brightness"] = brightness

        if color_kelvin and color_xy:
            logging.warning("Both color temperature and CIE 1931 x,y"
                            " color coordinates we provided to setState."
                            "Using color temperature and ignoring"
                            " CIE 1931 values.")

        if color_kelvin:
            values["desired_state"]["color_model"] = "color_temperature"
            values["desired_state"]["color_temperature"] = color_kelvin
        elif color_xy:
            values["desired_state"]["color_model"] = "xy"
            color_xy_iter = iter(color_xy)
            values["desired_state"]["color_x"] = next(color_xy_iter)
            values["desired_state"]["color_y"] = next(color_xy_iter)

        url_string = "{}/light_bulbs/{}".format(BASE_URL, self.device_id())
        arequest = requests.put(url_string,
                                data=json.dumps(values), headers=HEADERS)
        self._update_state_from_response(arequest.json())

        self._last_call = (time.time(), state)

    def __repr__(self):
        return "<Wink Bulb %s %s %s>" % (
            self.name(), self.device_id(), self.state())


class WinkLock(WinkDevice):
    """ represents a wink.py lock
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:

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

    def __init__(self, device_state_as_json, objectprefix="locks"):
        super(WinkLock, self).__init__(device_state_as_json,
                                       objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink lock %s %s %s>" % (self.name(),
                                         self.device_id(), self.state())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('locked', False)

    def device_id(self):
        return self.json_state.get('lock_id', self.name())

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        url_string = "{}/{}/{}".format(BASE_URL,
                                       self.objectprefix, self.device_id())
        values = {"desired_state": {"locked": state}}
        arequest = requests.put(url_string,
                                data=json.dumps(values), headers=HEADERS)
        self._update_state_from_response(arequest.json())

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_locked') == last_read.get('locked') \
                    or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkPowerStripOutlet(WinkDevice):
    """ represents a wink.py switch
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:

{
   "errors":[

   ],
   "data":{
      "powerstrip_id":"12345",
      "model_name":"Pivot Power Genius",
      "created_at":1451578768,
      "mac_address":"0c2a69000000",
      "locale":"en_us",
      "name":"Power strip",
      "units":{

      },
      "last_reading":{
         "connection":true,
         "connection_changed_at":1451947138.418391,
         "connection_updated_at":1452093346.488989
      },
      "triggers":[

      ],
      "location":"",
      "capabilities":{

      },
      "hidden_at":null,
      "outlets":[
         {
            "parent_object_type":"powerstrip",
            "icon_id":"4",
            "desired_state":{
               "powered":false
            },
            "parent_object_id":"24313",
            "scheduled_outlet_states":[

            ],
            "name":"Outlet #1",
            "outlet_index":0,
            "last_reading":{
               "desired_powered_updated_at":1452094688.1679382,
               "powered_updated_at":1452094688.1461067,
               "powered":false,
               "powered_changed_at":1452094688.1461067
            },
            "powered":false,
            "outlet_id":"48628"
         },
         {
            "parent_object_type":"powerstrip",
            "icon_id":"4",
            "desired_state":{
               "powered":false
            },
            "parent_object_id":"24313",
            "scheduled_outlet_states":[

            ],
            "name":"Outlet #2",
            "outlet_index":1,
            "last_reading":{
               "desired_powered_updated_at":1452094689.7589157,
               "powered_updated_at":1452094689.443459,
               "powered":false,
               "powered_changed_at":1452094689.443459
            },
            "powered":false,
            "outlet_id":"48629"
         }
      ],
      "serial":"AAAA00012345",
      "lat_lng":[
         00.000000,
         -00.000000
      ],
      "desired_state":{

      },
      "device_manufacturer":"quirky_ge",
      "upc_id":"24",
      "upc_code":"814434017226"
   },
   "pagination":{

   }
}

     """

    def __init__(self, device_state_as_json, objectprefix="powerstrips"):
        super(WinkPowerStripOutlet, self).__init__(device_state_as_json,
                                                   objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink" \
               " Power strip Outlet %s %s %s %s>" % (self.name(),
                                                     self.device_id(),
                                                     self.parent_id(),
                                                     self.state())

    @property
    def _last_reading(self):
        return self.json_state.get('last_reading') or {}

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        power_strip = response_json.get('data')
        outlets = power_strip.get('outlets', power_strip)
        for outlet in outlets:
            if outlet.get('outlet_id') == str(self.device_id()):
                self.json_state = outlet

    def update_state(self):
        """ Update state with latest info from Wink API. """
        url_string = "{}/{}/{}".format(BASE_URL,
                                       self.objectprefix, self.parent_id())
        arequest = requests.get(url_string, headers=HEADERS)
        self._update_state_from_response(arequest.json())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('powered', False)

    def index(self):
        return self.json_state.get('outlet_index', None)

    def device_id(self):
        return self.json_state.get('outlet_id', self.name())

    def parent_id(self):
        return self.json_state.get('parent_object_id',
                                   self.json_state.get('powerstrip_id'))

    # pylint: disable=unused-argument
    # kwargs is unused here but is used by child implementations
    def set_state(self, state, **kwargs):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        url_string = "{}/{}/{}".format(BASE_URL,
                                       self.objectprefix, self.parent_id())
        if self.index() == 0:
            values = {"outlets": [{"desired_state": {"powered": state}}, {}]}
        else:
            values = {"outlets": [{}, {"desired_state": {"powered": state}}]}

        arequest = requests.put(url_string,
                                data=json.dumps(values), headers=HEADERS)
        self._update_state_from_response(arequest.json())

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_powered') == last_read.get('powered') \
                    or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkGarageDoor(WinkDevice):
    r""" represents a wink.py garage door
    json_obj holds the json stat at init (and if there is a refresh it's updated
    it's the native format for this objects methods
    and looks like so:

{
  "data": {
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
  },
  "errors": [

  ],
  "pagination": {

  }
}
"""

    def __init__(self, device_state_as_json, objectprefix="garage_doors"):
        super(WinkGarageDoor, self).__init__(device_state_as_json,
                                             objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink garage door %s %s %s>" % (self.name(), self.device_id(), self.state())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('position', 0)

    def device_id(self):
        return self.json_state.get('garage_door_id', self.name())

    def set_state(self, state):
        """
        :param state:   a number of 1 ('open') or 0 ('close')
        :return: nothing
        """
        url_string = "{}/{}/{}".format(BASE_URL, self.objectprefix, self.device_id())
        values = {"desired_state": {"position": state}}
        arequest = requests.put(url_string, data=json.dumps(values), headers=HEADERS)
        self._update_state_from_response(arequest.json())

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_position') == last_read.get('0.0') \
               or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


def get_devices(filter_key):
    arequest_url = "{}/users/me/wink_devices".format(BASE_URL)
    j = requests.get(arequest_url, headers=HEADERS).json()

    items = j.get('data')

    devices = []
    for item in items:
        value_at_key = item.get(filter_key)
        if value_at_key is not None and item.get("hidden_at") is None:
            if filter_key == "powerstrip_id":
                outlets = item['outlets']
                for outlet in outlets:
                    value_at_key = outlet.get('outlet_id')
                    if (value_at_key is not None and
                            outlet.get("hidden_at") is None):
                        devices.append(WinkDevice.factory(outlet))
            else:
                devices.append(WinkDevice.factory(item))

    return devices


def get_bulbs():
    return get_devices('light_bulb_id')


def get_switches():
    return get_devices('binary_switch_id')


def get_sensors():
    return get_devices('sensor_pod_id')


def get_locks():
    return get_devices('lock_id')


def get_eggtrays():
    return get_devices('eggtray_id')


def get_garage_doors():
    return get_devices('garage_door_id')


def get_powerstrip_outlets():
    return get_devices('powerstrip_id')


def is_token_set():
    """ Returns if an auth token has been set. """
    return bool(HEADERS)


def set_bearer_token(token):
    global HEADERS

    HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
