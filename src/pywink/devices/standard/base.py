import time

from pywink.devices.base import WinkDevice


class WinkBinarySwitch(WinkDevice):
    """ represents a wink.py switch
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    """

    def __init__(self, device_state_as_json, api_interface, objectprefix="binary_switches"):
        super(WinkBinarySwitch, self).__init__(device_state_as_json, api_interface,
                                               objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink switch %s %s %s>" % (self.name(),
                                           self.device_id(), self.state())

    def state(self):
        if not self._last_reading.get('connection', False):
            return False
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
        values = {
            "desired_state": {
                "powered": state
            }
        }
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

        self._last_call = (time.time(), state)
