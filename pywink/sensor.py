from pywink.base import WinkDevice


class WinkSensorPod(WinkDevice):
    """
    A Wink "Sensor Pod" represents a single sensor.  Multi-sensor devices will be exposed as individual WinkSensorPods
    with a common root_id.
    """

    def __init__(self, device_state_as_json, objectprefix="sensor_pods"):
        super(WinkSensorPod, self).__init__(device_state_as_json,
                                            objectprefix=objectprefix)

    def __repr__(self):
        return "<Wink sensor %s %s %s>" % (self.name(),
                                           self.device_id(), self.state())

    def root_id(self):
        return None

    def state(self):
        if 'opened' in self._last_reading:
            return self._last_reading['opened']
        elif 'motion' in self._last_reading:
            return self._last_reading['motion']
        return False

    def device_id(self):
        return self.json_state.get('sensor_pod_id', self.name())
