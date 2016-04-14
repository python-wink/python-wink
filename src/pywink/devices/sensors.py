# -*- coding: utf-8 -*-
from pywink.devices.base import WinkDevice


class _WinkCapabilitySensor(WinkDevice):

    def __init__(self, device_state_as_json, api_interface, capability, unit):
        super(_WinkCapabilitySensor, self).__init__(device_state_as_json, api_interface,
                                                    objectprefix="sensor_pods")
        self._capability = capability
        self.unit = unit

    def __repr__(self):
        return "<Wink sensor {name} {dev_id} {reading}{unit}>".format(name=self.name(),
                                                                      dev_id=self.device_id(),
                                                                      reading=self._last_reading.get(self._capability),
                                                                      unit='' if self.unit is None else self.unit)

    def state(self):
        return self._last_reading.get('connection', False)

    def last_reading(self):
        return self._last_reading.get(self._capability)

    def capability(self):
        return self._capability

    def name(self):
        name = self.json_state.get('name', "Unknown Name")
        if self._capability != "opened":
            name += " " + self._capability
        return name

    @property
    def battery_level(self):
        if not self._last_reading.get('external_power', False):
            return self._last_reading.get('battery', False)
        else:
            return False

    def device_id(self):
        root_name = self.json_state.get('sensor_pod_id', self.name())
        return '{}+{}'.format(root_name, self._capability)

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        root_name = self.json_state.get('sensor_pod_id', self.name())
        response = self.api_interface.get_device_state(self, root_name)
        self._update_state_from_response(response,
                                         require_desired_state_fulfilled=require_desired_state_fulfilled)


class WinkSensorPod(_WinkCapabilitySensor):
    """ represents a wink.py sensor
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:
    """
    CAPABILITY = 'opened'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSensorPod, self).__init__(device_state_as_json, api_interface,
                                            self.CAPABILITY, self.UNIT)

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


class WinkHumiditySensor(_WinkCapabilitySensor):

    CAPABILITY = 'humidity'
    UNIT = '%'

    def __init__(self, device_state_as_json, api_interface):
        super(WinkHumiditySensor, self).__init__(device_state_as_json, api_interface,
                                                 self.CAPABILITY,
                                                 self.UNIT)

    def humidity_percentage(self):
        """
        :return: The relative humidity detected by the sensor (0% to 100%)
        :rtype: int
        """
        return self.last_reading()


class WinkBrightnessSensor(_WinkCapabilitySensor):

    CAPABILITY = 'brightness'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkBrightnessSensor, self).__init__(device_state_as_json, api_interface,
                                                   self.CAPABILITY,
                                                   self.UNIT)

    def brightness_boolean(self):
        """
        :return: True if light is detected.  False if light is below detection threshold (varies by device)
        :rtype: bool
        """
        return self.last_reading()


class WinkSoundPresenceSensor(_WinkCapabilitySensor):

    CAPABILITY = 'loudness'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSoundPresenceSensor, self).__init__(device_state_as_json, api_interface,
                                                      self.CAPABILITY,
                                                      self.UNIT)

    def loudness_boolean(self):
        """
        :return: True if sound is detected.  False if sound is below detection threshold (varies by device)
        :rtype: bool
        """
        return self.last_reading()


class WinkTemperatureSensor(_WinkCapabilitySensor):

    CAPABILITY = 'temperature'
    UNIT = u'\N{DEGREE SIGN}'

    def __init__(self, device_state_as_json, api_interface):
        super(WinkTemperatureSensor, self).__init__(device_state_as_json, api_interface,
                                                    self.CAPABILITY,
                                                    self.UNIT)

    def temperature_float(self):
        """
        :return: A float indicating the temperature.  Units are determined by the sensor.
        :rtype: float
        """
        return self.last_reading()


class WinkVibrationPresenceSensor(_WinkCapabilitySensor):

    CAPABILITY = 'vibration'
    UNIT = None

    def __init__(self, device_state_as_json, api_interface):
        super(WinkVibrationPresenceSensor, self).__init__(device_state_as_json, api_interface,
                                                          self.CAPABILITY,
                                                          self.UNIT)

    def vibration_boolean(self):
        """
        :return: Returns True if vibration is detected.
        :rtype: bool
        """
        return self.last_reading()
