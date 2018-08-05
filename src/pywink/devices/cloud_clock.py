from ..devices.base import WinkDevice


class WinkCloudClock(WinkDevice):
    """
    Represents a Quirky Nimbus.
    """

    def state(self):
        return self.available()

    def set_dial(self, json_value, index):
        """
        :param json_value: The value to set
        :param index: The dials index
        :return:
        """

        values = self.json_state
        json_value["channel_configuration"] = {"channel_id": "10"}
        values["dials"][index] = json_value

        response = self.api_interface.set_device_state(self, values)
        return response


class WinkCloudClockAlarm(WinkDevice):
    """
    Represents a Quirky Nimbus alarm.
    """

    def __init__(self, device_state_as_json, api_interface):
        super().__init__(device_state_as_json, api_interface)
        self.parent = None

    def state(self):
        return self.json_state('state')

    def set_parent(self, parent):
        self.parent = parent

    def available(self):
        return self.json_state.get('connection', False)


class WinkCloudClockDial(WinkDevice):
    """
    Represents a Quirky nimbus dial.
    """

    def __init__(self, device_state_as_json, api_interface):
        super().__init__(device_state_as_json, api_interface)
        self.parent = None

    def state(self):
        return self.json_state.get('value')

    def position(self):
        return self.json_state.get('position')

    def labels(self):
        return self.json_state.get('labels')

    def rotation(self):
        return self.json_state.get('rotation')

    def max_value(self):
        return self.json_state.get('max_value')

    def min_value(self):
        return self.json_state.get('min_value')

    def ticks(self):
        return self.json_state.get('ticks')

    def min_position(self):
        return self.json_state.get('min_position')

    def max_position(self):
        return self.json_state.get('max_position')

    def available(self):
        return self.json_state.get('connection', False)

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self, id_override=self.parent_id(),
                                                       type_override=self.parent_object_type())
        self._update_state_from_response(response)

    def set_parent(self, parent):
        self.parent = parent

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        cloud_clock = response_json.get('data')

        if cloud_clock is None:
            return False

        cloud_clock_last_reading = cloud_clock.get('last_reading')
        dials = cloud_clock.get('dials')
        for dial in dials:
            if dial.get('object_id') == self.object_id():
                dial['connection'] = cloud_clock_last_reading.get('connection')
                self.json_state = dial
                return True
        return False

    def pubnub_update(self, json_response):
        self._update_state_from_response(json_response)

    def index(self):
        return self.json_state.get('dial_index', None)

    def parent_id(self):
        return self.json_state.get('parent_object_id')

    def parent_object_type(self):
        return self.json_state.get('parent_object_type')

    def set_name(self, name):
        value = self.parent.json_state
        _json = {"name": name}
        value["dials"][self.index()] = _json
        response = self.api_interface.set_device_state(self, value, self.parent_id(), self.parent_object_type())
        self._update_state_from_response(response)

    def set_configuration(self, min_value, max_value, rotation="cw", scale="linear", ticks=12, min_position=0,
                          max_position=360):
        """

        :param min_value: Any number
        :param max_value: Any number above min_value
        :param rotation: (String) cw or ccw
        :param scale: (String) Linear and ...
        :param ticks:(Int) number of ticks of the clock up to 360?
        :param min_position: (Int) 0-360
        :param max_position: (Int) 0-360
        :return:
        """

        _json = {"min_value": min_value, "max_value": max_value, "rotation": rotation, "scale": scale, "ticks": ticks,
                 "min_position": min_position, "max_position": max_position}

        dial_config = {"dial_configuration": _json}

        self._update_state_from_response(self.parent.set_dial(dial_config, self.index()))

    def set_state(self, value, labels=None):
        """

        :param value: Any number
        :param labels: A list of two Strings sending None won't change the current values.
        :return:
        """

        values = {"value": value}
        json_labels = []
        if labels:
            for label in labels:
                json_labels.append(str(label).upper())
            values["labels"] = json_labels

        self._update_state_from_response(self.parent.set_dial(values, self.index()))
