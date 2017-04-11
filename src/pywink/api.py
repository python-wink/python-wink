import json
import time

import requests

from pywink.devices import types as device_types
from pywink.devices.factory import build_device

API_HEADERS = {}
CLIENT_ID = None
CLIENT_SECRET = None
REFRESH_TOKEN = None
USER_AGENT = "Manufacturer/python-wink python/3 Wink/3"
ALL_DEVICES = None
LAST_UPDATE = None


class WinkApiInterface(object):

    BASE_URL = "https://api.wink.com"

    def set_device_state(self, device, state, id_override=None, type_override=None):
        """
        :type device: WinkDevice
        :param state:   a boolean of true (on) or false ('off')
        :return: The JSON response from the API (new device state)
        """
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}".format(self.BASE_URL,
                                        object_type,
                                        object_id)
        if state is None:
            url_string += "/activate"
            arequest = requests.post(url_string,
                                     headers=API_HEADERS)
        else:
            arequest = requests.put(url_string,
                                    data=json.dumps(state),
                                    headers=API_HEADERS)
        if arequest.status_code == 401:
            new_token = refresh_access_token()
            if new_token:
                arequest = requests.put(url_string,
                                        data=json.dumps(state),
                                        headers=API_HEADERS)
            else:
                raise WinkAPIException("Failed to refresh access token.")
        print(str(arequest.json()))
        return arequest.json()

    def get_device_state(self, device, id_override=None, type_override=None):
        """
        :type device: WinkDevice
        """
        object_id = id_override or device.object_id()
        object_type = type_override or device.object_type()
        url_string = "{}/{}s/{}".format(self.BASE_URL,
                                        object_type, object_id)
        arequest = requests.get(url_string, headers=API_HEADERS)
        return arequest.json()


def get_set_access_token():
    auth = API_HEADERS.get("Authorization")
    if auth is not None:
        return auth.split()[1]
    else:
        return None


def set_bearer_token(token):
    global API_HEADERS

    API_HEADERS = {
        "Content-Type": "application/json",
        "Authorization": "Bearer {}".format(token)
    }
    if USER_AGENT:
        API_HEADERS["User-Agent"] = USER_AGENT


def set_user_agent(user_agent):
    global USER_AGENT

    USER_AGENT = user_agent


def set_wink_credentials(email, password, client_id, client_secret):
    global CLIENT_ID, CLIENT_SECRET, REFRESH_TOKEN

    CLIENT_ID = client_id
    CLIENT_SECRET = client_secret

    data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "password",
        "email": email,
        "password": password
    }
    headers = {
        'Content-Type': 'application/json'
    }
    response = requests.post('{}/oauth2/token'.format(WinkApiInterface.BASE_URL),
                             data=json.dumps(data),
                             headers=headers)
    response_json = response.json()
    access_token = response_json.get('access_token')
    REFRESH_TOKEN = response_json.get('refresh_token')
    set_bearer_token(access_token)


def refresh_access_token():
    if CLIENT_ID and CLIENT_SECRET and REFRESH_TOKEN:
        data = {
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN
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
    else:
        return None


def get_user():
    url_string = "{}/users/me".format(WinkApiInterface.BASE_URL)
    arequest = requests.get(url_string, headers=API_HEADERS)
    return arequest.json()


def is_token_set():
    """ Returns if an auth token has been set. """
    return bool(API_HEADERS)


def get_all_devices():
    return get_devices(device_types.ALL_SUPPORTED_DEVICES)


def get_light_bulbs():
    return get_devices(device_types.LIGHT_BULB)


def get_switches():
    return get_devices(device_types.BINARY_SWITCH)


def get_sensors():
    return get_devices(device_types.SENSOR_POD)


def get_locks():
    return get_devices(device_types.LOCK)


def get_eggtrays():
    return get_devices(device_types.EGGTRAY)


def get_garage_doors():
    return get_devices(device_types.GARAGE_DOOR)


def get_shades():
    return get_devices(device_types.SHADE)


def get_powerstrips():
    return get_devices(device_types.POWERSTRIP)


def get_sirens():
    return get_devices(device_types.SIREN)


def get_keys():
    return get_devices(device_types.KEY)


def get_piggy_banks():
    return get_devices(device_types.PIGGY_BANK)


def get_smoke_and_co_detectors():
    return get_devices(device_types.SMOKE_DETECTOR)


def get_thermostats():
    return get_devices(device_types.THERMOSTAT)


def get_hubs():
    return get_devices(device_types.HUB)


def get_fans():
    return get_devices(device_types.FAN)


def get_door_bells():
    return get_devices(device_types.DOOR_BELL)


def get_remotes():
    return get_devices(device_types.REMOTE)


def get_sprinklers():
    return get_devices(device_types.SPRINKLER)


def get_buttons():
    return get_devices(device_types.BUTTON)


def get_gangs():
    return get_devices(device_types.GANG)


def get_cameras():
    return get_devices(device_types.CAMERA)


def get_air_conditioners():
    return get_devices(device_types.AIR_CONDITIONER)


def get_propane_tanks():
    return get_devices(device_types.PROPANE_TANK)


def get_robots():
    return get_devices(device_types.ROBOT, "robots")


def get_scenes():
    return get_devices(device_types.SCENE, "scenes")


def get_subscription_key():
    response_dict = wink_api_fetch()
    first_device = response_dict.get('data')[0]
    return get_subscription_key_from_response_dict(first_device)


def get_subscription_key_from_response_dict(device):
    if "subscription" in device:
        return device.get("subscription").get("pubnub").get("subscribe_key")
    else:
        return None


def wink_api_fetch(end_point='wink_devices'):
    arequest_url = "{}/users/me/{}".format(WinkApiInterface.BASE_URL, end_point)
    response = requests.get(arequest_url, headers=API_HEADERS)
    if response.status_code == 200:
        return response.json()

    if response.status_code == 401:
        raise WinkAPIException("401 Response from Wink API.  Maybe Bearer token is expired?")
    else:
        raise WinkAPIException("Unexpected")


def get_devices(device_type, end_point="wink_devices"):
    global ALL_DEVICES, LAST_UPDATE

    if end_point == "wink_devices":
        now = time.time()
        # Only call the API once to obtain all devices
        if LAST_UPDATE is None or (now - LAST_UPDATE) > 60:
            ALL_DEVICES = wink_api_fetch(end_point)
            LAST_UPDATE = now
        return get_devices_from_response_dict(ALL_DEVICES, device_type)
    elif end_point == "robots" or end_point == "scenes":
        json_data = wink_api_fetch(end_point)
        return get_devices_from_response_dict(json_data, device_type)


def get_devices_from_response_dict(response_dict, device_type):
    """
    :rtype: list of WinkDevice
    """
    items = response_dict.get('data')

    devices = []

    api_interface = WinkApiInterface()

    for item in items:
        if item.get("object_type") in device_type:
            _devices = build_device(item, api_interface)
            for device in _devices:
                devices.append(device)

    return devices


class WinkAPIException(Exception):
    pass
