from ..devices.base import WinkDevice


class WinkRobot(WinkDevice):
    """
    Represents a Wink robot.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkRobot, self).__init__(device_state_as_json, api_interface)
        self._available = True
        self._capability = "fired"
        self._unit = None

    def state(self):
        return self._last_reading.get(self.capability(), False)

    def available(self):
        """
        Robots are virtual therefore they don't have a connection status
        always return True.
        """
        return self._available

    def unit(self):
        # Robots are a boolean sensor, they have no unit.
        return self._unit

    def capability(self):
        return self._capability
