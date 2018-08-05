"""
Build Wink devices.
"""

from ..devices import types as device_types
from ..devices.sensor import WinkSensor
from ..devices.light_bulb import WinkLightBulb
from ..devices.binary_switch import WinkBinarySwitch
from ..devices.lock import WinkLock
from ..devices.eggtray import WinkEggtray
from ..devices.garage_door import WinkGarageDoor
from ..devices.shade import WinkShade
from ..devices.siren import WinkSiren
from ..devices.key import WinkKey
from ..devices.thermostat import WinkThermostat
from ..devices.fan import WinkFan, WinkGeZwaveFan
from ..devices.remote import WinkRemote
from ..devices.hub import WinkHub
from ..devices.powerstrip import WinkPowerStrip, WinkPowerStripOutlet
from ..devices.piggy_bank import WinkPorkfolioBalanceSensor, WinkPorkfolioNose
from ..devices.sprinkler import WinkSprinkler
from ..devices.button import WinkButton
from ..devices.gang import WinkGang
from ..devices.smoke_detector import WinkSmokeDetector, WinkSmokeSeverity, WinkCoDetector, WinkCoSeverity
from ..devices.camera import WinkCanaryCamera
from ..devices.air_conditioner import WinkAirConditioner
from ..devices.propane_tank import WinkPropaneTank
from ..devices.robot import WinkRobot
from ..devices.scene import WinkScene
from ..devices.light_group import WinkLightGroup
from ..devices.binary_switch_group import WinkBinarySwitchGroup
from ..devices.water_heater import WinkWaterHeater
from ..devices.shade_group import WinkShadeGroup
from ..devices.cloud_clock import WinkCloudClock, WinkCloudClockDial, WinkCloudClockAlarm


# pylint: disable=too-many-branches, too-many-statements
def build_device(device_state_as_json, api_interface):
    # This is used to determine what type of object to create
    object_type = get_object_type(device_state_as_json)
    new_objects = []

    if object_type == device_types.LIGHT_BULB:
        new_objects.append(WinkLightBulb(device_state_as_json, api_interface))
    elif object_type == device_types.BINARY_SWITCH:
        # Skip relay switches that aren't controlling a load. The binary_switch can't be used.
        if device_state_as_json.get("last_reading").get("powering_mode") is not None:
            mode = device_state_as_json["last_reading"]["powering_mode"]
            if mode == "dumb":
                new_objects.append(WinkBinarySwitch(device_state_as_json, api_interface))
        else:
            new_objects.append(WinkBinarySwitch(device_state_as_json, api_interface))
    elif object_type == device_types.LOCK:
        new_objects.append(WinkLock(device_state_as_json, api_interface))
    elif object_type == device_types.EGGTRAY:
        new_objects.append(WinkEggtray(device_state_as_json, api_interface))
    elif object_type == device_types.GARAGE_DOOR:
        new_objects.append(WinkGarageDoor(device_state_as_json, api_interface))
    elif object_type == device_types.SHADE:
        new_objects.append(WinkShade(device_state_as_json, api_interface))
    elif object_type == device_types.SIREN:
        new_objects.append(WinkSiren(device_state_as_json, api_interface))
    elif object_type == device_types.KEY:
        new_objects.append(WinkKey(device_state_as_json, api_interface))
    elif object_type == device_types.THERMOSTAT:
        new_objects.append(WinkThermostat(device_state_as_json, api_interface))
    elif object_type == device_types.FAN:
        if __is_ge_zwave_fan(device_state_as_json):
            new_objects.append(WinkGeZwaveFan(device_state_as_json, api_interface))
        else:
            new_objects.append(WinkFan(device_state_as_json, api_interface))
    elif object_type == device_types.REMOTE:
        # The lutron Pico remote doesn't follow the API spec and
        # provides no benefit as a device in this library.
        if device_state_as_json.get("model_name") != "Pico":
            new_objects.append(WinkRemote(device_state_as_json, api_interface))
    elif object_type == device_types.HUB:
        new_objects.append(WinkHub(device_state_as_json, api_interface))
    elif object_type == device_types.SENSOR_POD:
        new_objects.extend(__get_subsensors_from_device(device_state_as_json, api_interface))
    elif object_type == device_types.POWERSTRIP:
        new_objects.extend(__get_outlets_from_powerstrip(device_state_as_json, api_interface))
        new_objects.append(WinkPowerStrip(device_state_as_json, api_interface))
    elif object_type == device_types.PIGGY_BANK:
        new_objects.extend(__get_devices_from_piggy_bank(device_state_as_json, api_interface))
    elif object_type == device_types.DOOR_BELL:
        new_objects.extend(__get_subsensors_from_device(device_state_as_json, api_interface))
    elif object_type == device_types.SPRINKLER:
        new_objects.append(WinkSprinkler(device_state_as_json, api_interface))
    elif object_type == device_types.BUTTON:
        new_objects.append(WinkButton(device_state_as_json, api_interface))
    elif object_type == device_types.GANG:
        new_objects.append(WinkGang(device_state_as_json, api_interface))
    elif object_type == device_types.SMOKE_DETECTOR:
        new_objects.extend(__get_sensors_from_smoke_detector(device_state_as_json, api_interface))
    elif object_type == device_types.CAMERA:
        if device_state_as_json.get("device_manufacturer") == "canary":
            new_objects.append(WinkCanaryCamera(device_state_as_json, api_interface))
        else:
            new_objects.extend(__get_subsensors_from_device(device_state_as_json, api_interface))
    elif object_type == device_types.AIR_CONDITIONER:
        new_objects.append(WinkAirConditioner(device_state_as_json, api_interface))
    elif object_type == device_types.PROPANE_TANK:
        new_objects.append(WinkPropaneTank(device_state_as_json, api_interface))
    elif object_type == device_types.ROBOT:
        new_objects.append(WinkRobot(device_state_as_json, api_interface))
    elif object_type == device_types.SCENE:
        new_objects.append(WinkScene(device_state_as_json, api_interface))
    elif object_type == device_types.GROUP:
        # This will skip auto created groups that Wink creates as well has empty groups
        if device_state_as_json.get("name")[0] not in [".", "@"] and device_state_as_json.get("members"):
            # This is a group of shades
            if device_state_as_json.get("reading_aggregation").get("position") is not None:
                new_objects.append(WinkShadeGroup(device_state_as_json, api_interface))
            # This is a group of switches
            elif device_state_as_json.get("reading_aggregation").get("brightness") is None:
                new_objects.append(WinkBinarySwitchGroup(device_state_as_json, api_interface))
            # This is a group of lights
            else:
                new_objects.append(WinkLightGroup(device_state_as_json, api_interface))
    elif object_type == device_types.WATER_HEATER:
        new_objects.append(WinkWaterHeater(device_state_as_json, api_interface))
    elif object_type == device_types.CLOUD_CLOCK:
        cloud_clock = WinkCloudClock(device_state_as_json, api_interface)
        new_objects.extend(__get_dials_from_cloudclock(device_state_as_json, api_interface, cloud_clock))
        new_objects.extend(__get_alarms_from_cloudclock(device_state_as_json, api_interface, cloud_clock))

    return new_objects


def get_object_type(device_state_as_json):
    if __is_ge_zwave_fan(device_state_as_json):
        return device_types.FAN
    return device_state_as_json.get("object_type")


def __is_ge_zwave_fan(device_state_as_json):
    return device_state_as_json.get("manufacturer_device_model") == "ge_jasco_in_wall_fan"


def __get_subsensors_from_device(item, api_interface):
    sensor_types = item.get('capabilities', {}).get('fields', [])
    sensor_types.extend(item.get('capabilities', {}).get('sensor_types', []))

    # These are attributes of the sensor, not the main sensor to track.
    ignored_sensors = ["battery", "powered", "connection", "tamper_detected",
                       "external_power"]

    subsensors = []

    for sensor_type in sensor_types:
        if sensor_type.get("field") in ignored_sensors:
            continue
        else:
            subsensors.append(WinkSensor(item, api_interface, sensor_type))

    return subsensors


def __get_outlets_from_powerstrip(item, api_interface):
    _outlets = []
    outlets = item['outlets']
    for outlet in outlets:
        if 'subscription' in item:
            outlet['subscription'] = item['subscription']
        outlet['last_reading']['connection'] = item['last_reading']['connection']
        _outlets.append(WinkPowerStripOutlet(outlet, api_interface))
    return _outlets


def __get_devices_from_piggy_bank(item, api_interface):
    return [WinkPorkfolioBalanceSensor(item, api_interface),
            WinkPorkfolioNose(item, api_interface)]


def __get_sensors_from_smoke_detector(item, api_interface):
    sensors = [WinkSmokeDetector(item, api_interface),
               WinkCoDetector(item, api_interface)]
    if item.get("manufacturer_device_model") == "nest":
        sensors.append(WinkSmokeSeverity(item, api_interface))
        sensors.append(WinkCoSeverity(item, api_interface))
    return sensors


def __get_dials_from_cloudclock(item, api_interface, parent):
    _dials = []
    dials = item['dials']
    for dial in dials:
        if 'subscription' in item:
            dial['subscription'] = item['subscription']
        dial['connection'] = item['last_reading']['connection']
        dial_obj = WinkCloudClockDial(dial, api_interface)
        dial_obj.set_parent(parent)
        _dials.append(dial_obj)
    return _dials


def __get_alarms_from_cloudclock(item, api_interface, parent):
    _alarms = []
    alarms = item['alarms']
    for alarm in alarms:
        alarm['subscription'] = item['subscription']
        alarm['connection'] = item['last_reading']['connection']
        alarm_obj = WinkCloudClockAlarm(alarm, api_interface)
        alarm_obj.set_parent(parent)
        _alarms.append(alarm_obj)
    return _alarms
