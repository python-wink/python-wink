import json

import requests

from pywink.devices import types as device_types
from pywink.devices.factory import build_device
from pywink.devices.sensors import WinkSensorPod, WinkHumiditySensor, WinkBrightnessSensor, WinkSoundPresenceSensor, \
    WinkTemperatureSensor, WinkVibrationPresenceSensor
from pywink.devices.types import DEVICE_ID_KEYS

API_HEADERS = {}


class WinkApiInterface(object):

    BASE_URL = "https://winkapi.quirky.com"

    def set_device_state(self, device, state, id_override=None):
        """
        :type device: WinkDevice
        :param state:   a boolean of true (on) or false ('off')
        :return: The JSON response from the API (new device state)
        """
        _id = device.device_id()
        if id_override:
            _id = id_override
        url_string = "{}/{}/{}".format(self.BASE_URL,
                                       device.objectprefix, _id)
        arequest = requests.put(url_string,
                                data=json.dumps(state),
                                headers=API_HEADERS)
        return arequest.json()

    def get_device_state(self, device, id_override=None):
        """
        :type device: WinkDevice
        """
        device_id = id_override or device.device_id()
        url_string = "{}/{}/{}".format(self.BASE_URL,
                                       device.objectprefix, device_id)
        arequest = requests.get(url_string, headers=API_HEADERS)
        return arequest.json()


def set_bearer_token(token):
    global API_HEADERS

    API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }


def set_wink_credentials(client_id, client_secret, refresh_token):
    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "refresh_token",
        "refresh_token": refresh_token
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('{}/oauth2/token'.format(WinkApiInterface.BASE_URL),
                             data=json.dumps(data),
                             headers=headers)
    response_json = response.json()
    access_token = response_json.get('access_token')
    set_bearer_token(access_token)
    return access_token


def get_bulbs():
    return get_devices(device_types.LIGHT_BULB)


def get_switches():
    return get_devices(device_types.BINARY_SWITCH)


def get_sensors():
    return get_devices(device_types.SENSOR_POD)


def get_locks():
    return get_devices(device_types.LOCK)


def get_eggtrays():
    return get_devices(device_types.EGG_TRAY)


def get_garage_doors():
    return get_devices(device_types.GARAGE_DOOR)


def get_shades():
    return get_devices(device_types.SHADE)


def get_powerstrip_outlets():
    return get_devices(device_types.POWER_STRIP)


def get_sirens():
    return get_devices(device_types.SIREN)


def get_devices(device_type):
    arequest_url = "{}/users/me/wink_devices".format(WinkApiInterface.BASE_URL)
    response = requests.get(arequest_url, headers=API_HEADERS)
    if response.status_code == 200:
        response_dict = response.json()
        filter_key = DEVICE_ID_KEYS.get(device_type)
        return get_devices_from_response_dict(response_dict, filter_key)

    if response.status_code == 401:
        raise WinkAPIException("401 Response from Wink API.  Maybe Bearer token is expired?")
    else:
        raise WinkAPIException("Unexpected")


def get_devices_from_response_dict(response_dict, filter_key):
    """
    :rtype: list of WinkDevice
    """
    items = response_dict.get('data')

    devices = []

    keys = DEVICE_ID_KEYS.values()
    if filter_key:
        keys = [filter_key]

    api_interface = WinkApiInterface()

    for item in items:
        for key in keys:
            if not __device_is_visible(item, key):
                continue

            if key == "powerstrip_id":
                devices.extend(__get_outlets_from_powerstrip(item, api_interface))
                continue  # Don't capture the powerstrip itself as a device, only the individual outlets

            if key == "sensor_pod_id":
                subsensors = _get_subsensors_from_sensor_pod(item, api_interface)
                if subsensors:
                    devices.extend(subsensors)

            devices.append(build_device(item, api_interface))

    return devices


def _get_subsensors_from_sensor_pod(item, api_interface):

    capabilities = [cap['field'] for cap in item.get('capabilities', {}).get('fields', [])]
    if not capabilities:
        return

    subsensors = []

    if WinkHumiditySensor.CAPABILITY in capabilities:
        subsensors.append(WinkHumiditySensor(item, api_interface))

    if WinkBrightnessSensor.CAPABILITY in capabilities:
        subsensors.append(WinkBrightnessSensor(item, api_interface))

    if WinkSoundPresenceSensor.CAPABILITY in capabilities:
        subsensors.append(WinkSoundPresenceSensor(item, api_interface))

    if WinkTemperatureSensor.CAPABILITY in capabilities:
        subsensors.append(WinkTemperatureSensor(item, api_interface))

    if WinkVibrationPresenceSensor.CAPABILITY in capabilities:
        subsensors.append(WinkVibrationPresenceSensor(item, api_interface))

    if WinkSensorPod.CAPABILITY in capabilities:
        subsensors.append(WinkSensorPod(item, api_interface))

    return subsensors


def __get_outlets_from_powerstrip(item, api_interface):
    outlets = item['outlets']
    for outlet in outlets:
        if 'subscription' in item:
            outlet['subscription'] = item['subscription']
        outlet['last_reading']['connection'] = item['last_reading']['connection']
    return [build_device(outlet, api_interface) for outlet in outlets if __device_is_visible(outlet, 'outlet_id')]


def __device_is_visible(item, key):
    is_correctly_structured = bool(item.get(key))
    is_visible = not item.get('hidden_at')
    return is_correctly_structured and is_visible


def refresh_state_at_hub(device):
    """
    Tell hub to query latest status from device and upload to Wink.
    PS: Not sure if this even works..
    :type device: WinkDevice
    """
    url_string = "{}/{}/{}/refresh".format(WinkApiInterface.BASE_URL,
                                           device.objectprefix,
                                           device.device_id())
    requests.get(url_string, headers=API_HEADERS)


def is_token_set():
    """ Returns if an auth token has been set. """
    return bool(API_HEADERS)


class WinkAPIException(Exception):
    pass
