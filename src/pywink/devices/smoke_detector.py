from pywink.devices.sensor import WinkDevice


class WinkSmokeDetector(WinkDevice):
    """
    Represents a Wink Smoke detector.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSmokeDetector, self).__init__(device_state_as_json, api_interface)
        self._unit = None
        self._cap = "smoke_detected"
        self._unit_type = "boolean"

    def unit(self):
        return self._unit

    def unit_type(self):
        return self._unit_type

    def capability(self):
        return self._cap

    def name(self):
        return self.json_state.get("name") + " " + self.capability()

    def state(self):
        return self._last_reading.get(self.capability())


class WinkSmokeSeverity(WinkDevice):
    """
    Represents a Wink/Nest Smoke severity sensor.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkSmokeSeverity, self).__init__(device_state_as_json, api_interface)
        self._unit = None
        self._cap = "smoke_severity"
        self._unit_type = None

    def unit(self):
        return self._unit

    def unit_type(self):
        return self._unit_type

    def capability(self):
        return self._cap

    def name(self):
        return self.json_state.get("name") + " " + self.capability()

    def state(self):
        return self._last_reading.get(self.capability())


class WinkCoDetector(WinkDevice):
    """
    Represents a Wink CO detector.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkCoDetector, self).__init__(device_state_as_json, api_interface)
        self._unit = None
        self._cap = "co_detected"
        self._unit_type = "boolean"

    def unit(self):
        return self._unit

    def unit_type(self):
        return self._unit_type

    def capability(self):
        return self._cap

    def name(self):
        return self.json_state.get("name") + " " + self.capability()

    def state(self):
        return self._last_reading.get(self.capability())


class WinkCoSeverity(WinkDevice):
    """
    Represents a Wink/Nest CO severity sensor.
    """

    def __init__(self, device_state_as_json, api_interface):
        super(WinkCoSeverity, self).__init__(device_state_as_json, api_interface)
        self._unit = None
        self._cap = "co_severity"
        self._unit_type = None

    def unit(self):
        return self._unit

    def unit_type(self):
        return self._unit_type

    def capability(self):
        return self._cap

    def name(self):
        return self.json_state.get("name") + " " + self.capability()

    def state(self):
        return self._last_reading.get(self.capability())
