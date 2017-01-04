from pywink.devices.standard.base import WinkDevice


# pylint: disable=too-many-public-methods
class WinkFan(WinkDevice):
    """
    Represents a Wink fan
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods

    For example API responses, see unit tests.
     """
    json_state = {}

    def __init__(self, device_state_as_json, api_interface):
        super(WinkFan, self).__init__(device_state_as_json, api_interface,
                                      objectprefix="fans")

    def device_id(self):
        return self.json_state.get('fan_id', self.name())

    def fan_speeds(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_speeds = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'mode':
                fan_speeds = field.get('choices')
        return fan_speeds

    def fan_directions(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_directions = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'direction':
                fan_directions = field.get('choices')
        return fan_directions

    def fan_timer_range(self):
        capabilities = self.json_state.get('capabilities', {})
        cap_fields = capabilities.get('fields', [])
        fan_timer_range = None
        for field in cap_fields:
            _field = field.get('field')
            if _field == 'timer':
                fan_timer_range = field.get('range')
        return fan_timer_range

    def current_fan_speed(self):
        return self._last_reading.get('mode', None)

    def current_fan_direction(self):
        return self._last_reading.get('direction', None)

    def current_timer(self):
        return self._last_reading.get('timer', None)

    def state(self):
        return self._last_reading.get('powered', False)

    def set_state(self, state):
        """
        :param powered: bool
        :return: nothing
        """
        desired_state = {"powered": state}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_fan_speed(self, speed):
        """
        :param speed: a string one of ["lowest", "low",
            "medium", "high", "auto"]
        :return: nothing
        """
        desired_state = {"mode": speed}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_fan_direction(self, direction):
        """
        :param speed: a string one of ["forward", "reverse"]
        :return: nothing
        """
        desired_state = {"direction": direction}

        response = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(response)

    def set_fan_timer(self, timer):
        """
        :param timer: an int between fan_timer_range
        :return: nothing
        """
        desired_state = {"timer": timer}

        resp = self.api_interface.set_device_state(self, {
            "desired_state": desired_state
        })

        self._update_state_from_response(resp)

    def __repr__(self):
        return "<Wink Fan %s %s>" % (
            self.name(), self.device_id())
