from pywink.domain.devices import is_desired_state_reached


class WinkDevice(object):

    def __init__(self, device_state_as_json, api_interface, objectprefix=None):
        """
        :type api_interface pywink.api.WinkApiInterface:
        :return:
        """
        self.api_interface = api_interface
        self.objectprefix = objectprefix
        self.json_state = device_state_as_json

    def __str__(self):
        return "%s %s %s" % (self.name(), self.device_id(), self.state())

    def __repr__(self):
        return "<Wink object name:{name} id:{device} state:{state}>".format(name=self.name(),
                                                                            device=self.device_id(),
                                                                            state=self.state())

    def name(self):
        return self.json_state.get('name', "Unknown Name")

    def state(self):
        raise NotImplementedError("Must implement state")

    def device_id(self):
        raise NotImplementedError("Must implement device_id")

    @property
    def _last_reading(self):
        return self.json_state.get('last_reading') or {}

    @property
    def available(self):
        return self._last_reading.get('connection', False)

    def _update_state_from_response(self, response_json, require_desired_state_fulfilled=False):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        response_json = response_json.get('data')
        if response_json and require_desired_state_fulfilled:
            if not is_desired_state_reached(response_json):
                return
        self.json_state = response_json

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self)
        self._update_state_from_response(response, require_desired_state_fulfilled)
