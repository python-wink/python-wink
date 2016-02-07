"""
Objects for interfacing with the Wink API
"""
import logging
import time

from pywink.devices.base import WinkDevice


class WinkEggTray(WinkDevice):
    """ represents a wink.py egg tray
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    """

    def __init__(self, device_state_as_json, api_interface, objectprefix="eggtrays"):
        super(WinkEggTray, self).__init__(device_state_as_json, api_interface,
                                          objectprefix=objectprefix)

    def __repr__(self):
        return "<Wink eggtray name:{name} id:{device} state:{state}>".format(name=self.name(),
                                                                             device=self.device_id(),
                                                                             state=self.state())

    def state(self):
        if 'inventory' in self._last_reading:
            return self._last_reading['inventory']
        return False

    def device_id(self):
        return self.json_state.get('eggtray_id', self.name())


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
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

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
        response = self.api_interface.set_device_state(self, state)
        self._update_state_from_response(response)

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_powered') == last_read.get('powered') or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkBulb(WinkBinarySwitch):
    """
    Represents a Wink light bulb
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods

    For example API responses, see unit tests.
     """
    json_state = {}

    def __init__(self, device_state_as_json, api_interface):
        super().__init__(device_state_as_json, api_interface,
                         objectprefix="light_bulbs")

    def device_id(self):
        return self.json_state.get('light_bulb_id', self.name())

    def brightness(self):
        return self._last_reading.get('brightness')

    def color_xy(self):
        """
        XY colour value: [float, float] or None
        :rtype: list float
        """
        color_x = self._last_reading.get('color_x')
        color_y = self._last_reading.get('color_y')

        if color_x and color_y:
            return [float(color_x), float(color_y)]

        return None

    def color_temperature_kelvin(self):
        """
        Color temperature, in degrees Kelvin.
        Eg: "Daylight" light bulbs are 4600K
        :rtype: int
        """
        return self._last_reading.get('color_temperature')

    def set_state(self, state, brightness=None,
                  color_kelvin=None, color_xy=None, **kwargs):
        """
        :param state:   a boolean of true (on) or false ('off')
        :param brightness: a float from 0 to 1 to set the brightness of
         this bulb
        :param color_kelvin: an integer greater than 0 which is a color in
         degrees Kelvin
        :param color_xy: a pair of floats in a list which specify the desired
         CIE 1931 x,y color coordinates
        :return: nothing
        """
        values = {
            "desired_state": {
                "powered": state
            }
        }

        if brightness is not None:
            values["desired_state"]["brightness"] = brightness

        if color_kelvin and color_xy:
            logging.warning("Both color temperature and CIE 1931 x,y"
                            " color coordinates we provided to setState."
                            "Using color temperature and ignoring"
                            " CIE 1931 values.")

        if color_kelvin:
            values["desired_state"]["color_model"] = "color_temperature"
            values["desired_state"]["color_temperature"] = color_kelvin
        elif color_xy:
            values["desired_state"]["color_model"] = "xy"
            color_xy_iter = iter(color_xy)
            values["desired_state"]["color_x"] = next(color_xy_iter)
            values["desired_state"]["color_y"] = next(color_xy_iter)

        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

        self._last_call = (time.time(), state)

    def __repr__(self):
        return "<Wink Bulb %s %s %s>" % (
            self.name(), self.device_id(), self.state())


class WinkLock(WinkDevice):
    """
    represents a wink.py lock
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    """

    def __init__(self, device_state_as_json, api_interface, objectprefix="locks"):
        super(WinkLock, self).__init__(device_state_as_json, api_interface,
                                       objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink lock %s %s %s>" % (self.name(),
                                         self.device_id(), self.state())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('locked', False)

    def device_id(self):
        return self.json_state.get('lock_id', self.name())

    def set_state(self, state):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        values = {"desired_state": {"locked": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)
        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_locked') == last_read.get('locked') or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkPowerStripOutlet(WinkBinarySwitch):
    """ represents a wink.py switch
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    and looks like so:
    """

    def __init__(self, device_state_as_json, api_interface, objectprefix="powerstrips"):
        super(WinkPowerStripOutlet, self).__init__(device_state_as_json, api_interface,
                                                   objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink Power strip outlet name:{name} id:{device}" \
               " parent id:{parent_id} state:{state}>".format(name=self.name(),
                                                              device=self.device_id(),
                                                              parent_id=self.parent_id(),
                                                              state=self.state())

    @property
    def _last_reading(self):
        return self.json_state.get('last_reading') or {}

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        power_strip = response_json.get('data')
        power_strip_reading = power_strip.get('last_reading')
        outlets = power_strip.get('outlets', power_strip)
        for outlet in outlets:
            if outlet.get('outlet_id') == str(self.device_id()):
                outlet['last_reading']['connection'] = power_strip_reading.get('connection')
                self.json_state = outlet

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self)
        self._update_state_from_response(response)

    def index(self):
        return self.json_state.get('outlet_index', None)

    def device_id(self):
        return self.json_state.get('outlet_id', self.name())

    def parent_id(self):
        return self.json_state.get('parent_object_id',
                                   self.json_state.get('powerstrip_id'))

    # pylint: disable=unused-argument
    # kwargs is unused here but is used by child implementations
    def set_state(self, state, **kwargs):
        """
        :param state:   a boolean of true (on) or false ('off')
        :return: nothing
        """
        if self.index() == 0:
            values = {"outlets": [{"desired_state": {"powered": state}}, {}]}
        else:
            values = {"outlets": [{}, {"desired_state": {"powered": state}}]}

        response = self.api_interface.set_device_state(self, values, id_override=self.parent_id())
        self._update_state_from_response(response)

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_powered') == last_read.get('powered') or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkGarageDoor(WinkDevice):
    r""" represents a wink.py garage door
    json_obj holds the json stat at init (and if there is a refresh it's updated
    it's the native format for this objects methods
    and looks like so:
    """

    def __init__(self, device_state_as_json, api_interface, objectprefix="garage_doors"):
        super(WinkGarageDoor, self).__init__(device_state_as_json, api_interface,
                                             objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink garage door %s %s %s>" % (self.name(), self.device_id(), self.state())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('position', 0)

    def device_id(self):
        return self.json_state.get('garage_door_id', self.name())

    def set_state(self, state):
        """
        :param state:   a number of 1 ('open') or 0 ('close')
        :return: nothing
        """
        values = {"desired_state": {"position": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

        self._last_call = (time.time(), state)

    def wait_till_desired_reached(self):
        """ Wait till desired state reached. Max 10s. """
        if self._recent_state_set():
            return

        # self.refresh_state_at_hub()
        tries = 1

        while True:
            self.update_state()
            last_read = self._last_reading

            if last_read.get('desired_position') == last_read.get('0.0') \
               or tries == 5:
                break

            time.sleep(2)

            tries += 1
            self.update_state()
            last_read = self._last_reading

    def _recent_state_set(self):
        return time.time() - self._last_call[0] < 15


class WinkSiren(WinkBinarySwitch):
    """ represents a wink.py siren
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    """

    def __init__(self, device_state_as_json, api_interface, objectprefix="sirens"):
        super(WinkSiren, self).__init__(device_state_as_json, api_interface,
                                        objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink siren %s %s %s>" % (self.name(),
                                          self.device_id(), self.state())

    def device_id(self):
        return self.json_state.get('siren_id', self.name())
