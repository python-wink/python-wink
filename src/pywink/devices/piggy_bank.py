from ..devices.base import WinkDevice


class WinkPorkfolioNose(WinkDevice):
    """
    Represents a Wink Porkfolio nose.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkPorkfolioNose, self).__init__(device_state_as_json, api_interface)
        self._available = True

    def available(self):
        """
        connection variable isn't stable.
        Porkfolio can be offline, but updates will continue to occur.
        always returning True to avoid this issue.
        This is the same for the PorkFolio balance sensor.
        """
        return self._available

    def set_state(self, color_hex):
        """
        :param color_hex: a hex string indicating the color of the porkfolio nose
        :return: nothing
        From the api...
        "the color of the nose is not in the desired_state
        but on the object itself."
        """
        root_name = self.json_state.get('piggy_bank_id', self.name())
        response = self.api_interface.set_device_state(self, {
            "nose_color": color_hex
        }, root_name)
        self._update_state_from_response(response)

    def state(self):
        """
        Hex colour value: String or None
        :rtype: list float
        """
        return self.json_state.get('nose_color')

    def name(self):
        name = self.json_state.get('name')
        name += " Nose"
        return name


class WinkPorkfolioBalanceSensor(WinkDevice):
    """
    Represents a Wink Porkfolio balance sensor.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkPorkfolioBalanceSensor, self).__init__(device_state_as_json, api_interface)
        self._unit = 'USD'
        self._cap = 'balance'
        self._available = True

    def unit(self):
        return self._unit

    def capability(self):
        # Legacy device, doesn't have a capability list.
        return self._cap

    def state(self):
        return self._last_reading.get(self.capability())

    def name(self):
        name = self.json_state.get('name')
        name += " " + self.capability()
        return name

    def available(self):
        """
        connection variable isn't stable.
        Porkfolio can be offline, but updates will continue to occur.
        always returning True to avoid this issue.
        """
        return self._available

    def deposit(self, amount):
        """

        :param amount: (int +/-) amount to be deposited or withdrawn in cents
        """
        _json = {"amount": amount}
        self.api_interface.piggy_bank_deposit(self, _json)
