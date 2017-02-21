from pywink.devices.base import WinkDevice


class WinkScene(WinkDevice):
    """
    Represents a Wink scene.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkScene, self).__init__(device_state_as_json, api_interface)

    def state(self):
        """
        Scenes don't have a state, they can only be triggered.
        Always return a state of False.
        """
        return False

    def available(self):
        """
        Scenes are virtual therefore they don't have a connection status
        always return True.
        """
        return True

    def activate(self):
        """
        Activate the scene.
        """
        response = self.api_interface.set_device_state(self, None)
        self._update_state_from_response(response)

    def update_state(self):
        """
        Nothing changes in the JSON state of this device.
        """
        return True
