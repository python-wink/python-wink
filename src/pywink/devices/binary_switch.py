from pywink.devices.base import WinkDevice


class WinkBinarySwitch(WinkDevice):
    """
    Represents a Wink binary switch.
    """

    def state(self):
        return self._last_reading.get('powered', False)

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        values = {"desired_state": {"powered": state}}
        response = self.api_interface.local_set_state(self, values, type_override="binary_switche")
        self._update_state_from_response(response)

    def update_state(self):
        """
        Update state with latest info from Wink API.
        """
        response = self.api_interface.local_get_state(self, type_override="binary_switche")
        return self._update_state_from_response(response)


class WinkLeakSmartValve(WinkBinarySwitch):
    """
    Represents a Wink leaksmart valve..
    """

    def state(self):
        return self._last_reading.get('opened', False)

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        values = {"desired_state": {"opened": state}}
        response = self.api_interface.local_set_state(self, values, type_override="binary_switche")
        self._update_state_from_response(response)

    def last_event(self):
        return self._last_reading.get("last_event")

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.local_get_state(self)
        return self._update_state_from_response(response)
