from pywink.devices.base import WinkDevice


class WinkHub(WinkDevice):
    """
    Represents a Wink Hub.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkHub, self).__init__(device_state_as_json, api_interface)
        self._unit = None

    def unit(self):
        return self._unit

    def state(self):
        return self.available()

    def kidde_radio_code(self):
        config = self.json_state.get('configuration')
        return config.get('kidde_radio_code')

    def update_needed(self):
        return self._last_reading.get('update_needed')

    def ip_address(self):
        return self._last_reading.get('ip_address')

    def firmware_version(self):
        return self._last_reading.get('firmware_version')
