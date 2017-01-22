from pywink.devices.base import WinkDevice


class WinkShade(WinkDevice):
    """
    Represents a Wink Shade.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkShade, self).__init__(device_state_as_json, api_interface)

    def state(self):
        return self._last_reading.get('position', 0)

    def set_state(self, state):
        """
        :param state:   a number of 1 ('open') or 0 ('close')
        :return: nothing
        """
        values = {"desired_state": {"position": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)
