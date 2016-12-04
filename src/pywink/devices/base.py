

class WinkDevice(object):

    def __init__(self, device_state_as_json, api_interface, objectprefix=None):
        """
        :type api_interface pywink.api.WinkApiInterface:
        :return:
        """
        self.api_interface = api_interface
        self.objectprefix = objectprefix
        self.json_state = device_state_as_json
        subscription = self.json_state.get('subscription')
        if subscription != {} and subscription is not None:
            pubnub = subscription.get('pubnub')
            self.pubnub_key = pubnub.get('subscribe_key')
            self.pubnub_channel = pubnub.get('channel')
        else:
            self.pubnub_key = None
            self.pubnub_channel = None

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

    @property
    def battery_level(self):
        return self._last_reading.get('battery', None)

    @property
    def manufacturer_device_model(self):
        return self.json_state.get('manufacturer_device_model', None)

    @property
    def manufacturer_device_id(self):
        return self.json_state.get('manufacturer_device_id', None)

    @property
    def device_manufacturer(self):
        return self.json_state.get('device_manufacturer', None)

    @property
    def model_name(self):
        return self.json_state.get('model_name', None)

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        _response_json = response_json.get('data')
        self.json_state = _response_json
        return True

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self)
        return self._update_state_from_response(response)

    def pubnub_update(self, json_response):
        self.json_state = json_response
