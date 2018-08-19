from datetime import datetime
import logging
import random

from ..devices.base import WinkDevice


DTSTART = "DTSTART;TZID="
REPEAT = "RRULE:FREQ=WEEKLY;BYDAY="

_LOGGER = logging.getLogger(__name__)


class WinkCloudClock(WinkDevice):
    """
    Represents a Quirky Nimbus.
    """

    def state(self):
        return self.available()

    def set_dial(self, json_value, index, timezone=None):
        """
        :param json_value: The value to set
        :param index: The dials index
        :param timezone: The time zone to use for a time dial
        :return:
        """

        values = self.json_state
        if timezone is None:
            json_value["channel_configuration"] = {"channel_id": "10"}
            values["dials"][index] = json_value

            response = self.api_interface.set_device_state(self, values)
        else:
            json_value["channel_configuration"] = {"channel_id": "1", "timezone": timezone}
            values["dials"][index] = json_value
            response = self.api_interface.set_device_state(self, values)
        return response

    def get_time_dial(self):
        for dial in self.json_state.get("dials", {}):
            if dial['channel_configuration']['channel_id'] == "1":
                if dial['name'] == "Time":
                    return dial
                return None
        return None

    def create_alarm(self, date, days=None, name=None):
        if self.get_time_dial() is None:
            _LOGGER.error("Not creating alarm, no time dial.")
            return False
        timezone_string = self.get_time_dial()["channel_configuration"]["timezone"]
        ical_string = _create_ical_string(timezone_string, date, days)

        nonce = str(random.randint(0, 1000000000))

        _json = {'recurrence': ical_string, 'enabled': True, 'nonce': nonce}
        if name:
            _json['name'] = name
        self.api_interface.create_cloud_clock_alarm(self, _json)
        return True


class WinkCloudClockAlarm(WinkDevice):
    """
    Represents a Quirky Nimbus alarm.
    """

    def __init__(self, device_state_as_json, api_interface):
        super().__init__(device_state_as_json, api_interface)
        self.parent = None
        self.start_time, self.days = _parse_ical_string(device_state_as_json.get('recurrence'))

    def state(self):
        return self.json_state['next_at']

    def set_parent(self, parent):
        self.parent = parent

    def available(self):
        enabled = self.json_state['enabled']
        clock = self.parent.get_time_dial()
        return bool(enabled and clock is not None)

    def recurrence(self):
        return self.json_state['recurrence']

    def set_enabled(self, enabled):
        self.api_interface.set_device_state(self, {"enabled": enabled})

    def update_state(self):
        """ Update state with latest info from Wink API. """
        response = self.api_interface.get_device_state(self, id_override=self.parent.object_id(),
                                                       type_override=self.parent.object_type())
        self._update_state_from_response(response)

    def _update_state_from_response(self, response_json):
        """
        :param response_json: the json obj returned from query
        :return:
        """
        if 'data' in response_json and response_json['data']['object_type'] == "cloud_clock":
            cloud_clock = response_json.get('data')
            if cloud_clock is None:
                return False

            alarms = cloud_clock.get('alarms')
            for alarm in alarms:
                if alarm.get('object_id') == self.object_id():
                    self.json_state = alarm
                    return True
            return False
        if 'data' in response_json:
            alarm = response_json.get('data')
            self.json_state = alarm
            return True
        self.json_state = response_json
        return True

    def set_recurrence(self, date, days=None):
        """

        :param date: Datetime object time to start/repeat
        :param days: days to repeat (Defaults to one time alarm)
        :return:
        """
        if self.parent.get_time_dial() is None:
            _LOGGER.error("Not setting alarm, no time dial.")
            return False
        timezone_string = self.parent.get_time_dial()["channel_configuration"]["timezone"]
        ical_string = _create_ical_string(timezone_string, date, days)
        _json = {'recurrence': ical_string, 'enabled': True}

        self.api_interface.set_device_state(self, _json)
        return True


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
        return self.json_state['dial_configuration'].get('rotation')

    def max_value(self):
        return self.json_state['dial_configuration'].get('max_value')

    def min_value(self):
        return self.json_state['dial_configuration'].get('min_value')

    def ticks(self):
        return self.json_state['dial_configuration'].get('num_ticks')

    def min_position(self):
        return self.json_state['dial_configuration'].get('min_position')

    def max_position(self):
        return self.json_state['dial_configuration'].get('max_position')

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

    def make_time_dial(self, timezone_string):
        """

        :param timezone_string:
        :return:
        """
        self._update_state_from_response(self.parent.set_dial({}, self.index(), timezone_string))


def _create_ical_string(timezone_string, date, days=None):
    valid_days = ["SU", "MO", "TU", "WE", "TH", "FR", "SA"]
    ical_string = DTSTART + timezone_string + ":" + date.strftime("%Y%m%dT%H%M%S")
    if days is not None:
        if days == "DAILY":
            ical_string = ical_string + "\nRRULE:FREQ=DAILY"
        else:
            ical_string = ical_string + "\n" + REPEAT
            for day in days:
                if day in valid_days:
                    if ical_string[-1] == "=":
                        ical_string = ical_string + day
                    else:
                        ical_string = ical_string + ',' + day
                else:
                    error = "Invalid repeat day {}".format(day)

                    _LOGGER.error(error)

    return ical_string


def _parse_ical_string(ical_string):
    """
    SU,MO,TU,WE,TH,FR,SA
    DTSTART;TZID=America/New_York:20180804T233251\nRRULE:FREQ=WEEKLY;BYDAY=SA
    DTSTART;TZID=America/New_York:20180804T233251\nRRULE:FREQ=DAILY
    DTSTART;TZID=America/New_York:20180804T233251\nRRULE:FREQ=WEEKLY;BYDAY=MO,TU,WE,TH,FR,SA
    DTSTART;TZID=America/New_York:20180718T174500
    """
    start_time = ical_string.splitlines()[0].replace(DTSTART, '')
    if "RRULE" in ical_string:
        days = ical_string.splitlines()[1].replace(REPEAT, '')
        if days == "RRULE:FREQ=DAILY":
            days = ['DAILY']
        else:
            days = days.split(',')
    else:
        days = None
    start_time = start_time.splitlines()[0].split(':')[1]
    datetime_object = datetime.strptime(start_time, '%Y%m%dT%H%M%S')
    return datetime_object, days
