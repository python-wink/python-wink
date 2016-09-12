"""
Objects for interfacing with the Wink API
"""
import time

from pywink.devices.base import WinkDevice
from pywink.devices.standard.base import WinkBinarySwitch
from pywink.devices.standard.bulb import WinkBulb
from pywink.domain.devices import is_desired_state_reached


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

    # pylint: disable=duplicate-code
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

    def update_state(self, require_desired_state_fulfilled=False):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self, id_override=self.parent_id())
        power_strip = response.get('data')
        if require_desired_state_fulfilled:
            if not is_desired_state_reached(power_strip[self.index]):
                return

        power_strip_reading = power_strip.get('last_reading')
        outlets = power_strip.get('outlets', power_strip)
        for outlet in outlets:
            if outlet.get('outlet_id') == str(self.device_id()):
                outlet['last_reading']['connection'] = power_strip_reading.get('connection')
                self.json_state = outlet

    def _update_state_from_response(self, response_json, require_desired_state_fulfilled=False):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        power_strip = response_json
        power_strip_reading = power_strip.get('last_reading')
        outlets = power_strip.get('outlets', power_strip)
        for outlet in outlets:
            if outlet.get('outlet_id') == str(self.device_id()):
                outlet['last_reading']['connection'] = power_strip_reading.get('connection')
                self.json_state = outlet

    def pubnub_update(self, json_response):
        self._update_state_from_response(json_response)

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
        power_strip = response.get('data')
        self._update_state_from_response(power_strip)

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

    # pylint: disable=duplicate-code
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


class WinkShade(WinkDevice):
    def __init__(self, device_state_as_json, api_interface, objectprefix="shades"):
        super(WinkShade, self).__init__(device_state_as_json, api_interface,
                                        objectprefix=objectprefix)
        # Tuple (desired state, time)
        self._last_call = (0, None)

    def __repr__(self):
        return "<Wink shade %s %s %s>" % (self.name(),
                                          self.device_id(), self.state())

    def device_id(self):
        return self.json_state.get('shade_id', self.name())

    def state(self):
        # Optimistic approach to setState:
        # Within 15 seconds of a call to setState we assume it worked.
        if self._recent_state_set():
            return self._last_call[1]

        return self._last_reading.get('position', 0)

    def set_state(self, state):
        """
        :param state:   a number of 1 ('open') or 0 ('close')
        :return: nothing
        """
        values = {"desired_state": {"position": state}}
        response = self.api_interface.set_device_state(self, values)
        self._update_state_from_response(response)

        self._last_call = (time.time(), state)
        # self._state = state

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


class WinkKey(WinkDevice):
    """ represents a wink.py key
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods
    """
    UNIT = None

    def __init__(self, device_state_as_json, api_interface, objectprefix="keys"):
        super(WinkKey, self).__init__(device_state_as_json, api_interface,
                                      objectprefix=objectprefix)
        self._capability = "opening"

    def __repr__(self):
        return "<Wink key name:{name} id:{device}" \
               " parent id:{parent_id} state:{state}>".format(name=self.name(),
                                                              device=self.device_id(),
                                                              parent_id=self.parent_id(),
                                                              state=self.state())

    def state(self):
        if 'activity_detected' in self._last_reading:
            return self._last_reading['activity_detected']
        return False

    def device_id(self):
        return self.json_state.get('key_id', self.name())

    def parent_id(self):
        return self.json_state.get('parent_object_id',
                                   self.json_state.get('lock_id'))

    def capability(self):
        """Return opening for all keys."""
        return self._capability

    @property
    def available(self):
        """Keys are virtual therefore they don't have a connection status
        always return True
        """
        return True


class WinkPorkfolioNose(WinkDevice):
    """
    Represents a Wink Porkfolio nose
    json_obj holds the json stat at init (if there is a refresh it's updated)
    it's the native format for this objects methods

    For example API responses, see unit tests.
    """
    json_state = {}

    def __init__(self, device_state_as_json, api_interface):
        super().__init__(device_state_as_json, api_interface,
                         objectprefix="piggy_banks")

    @property
    def available(self):
        """
        connection variable isn't stable.
        Porkfolio can be offline, but updates will continue to occur.
        always returning True to avoid this issue.
        """
        return True

    def device_id(self):
        root_name = self.json_state.get('piggy_bank_id', self.name())
        return '{}+{}'.format(root_name, "nose")

    def set_state(self, color_hex):
        """
        :param nose_color: a hex string indicating the color of the porkfolio nose
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
        return self.json_state.get('nose_color', None)


# pylint-disable: undefined-all-variable
__all__ = [WinkEggTray.__name__,
           WinkBinarySwitch.__name__,
           WinkBulb.__name__,
           WinkLock.__name__,
           WinkPowerStripOutlet.__name__,
           WinkGarageDoor.__name__,
           WinkShade.__name__,
           WinkSiren.__name__,
           WinkPorkfolioNose.__name__]
