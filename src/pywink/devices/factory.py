from pywink.devices.base import WinkDevice
from pywink.devices.sensors import WinkSensorPod
from pywink.devices.standard import WinkBulb, WinkBinarySwitch, WinkPowerStripOutlet, WinkLock, \
    WinkEggTray, WinkGarageDoor, WinkShade, WinkSiren, WinkKey, WinkThermostat, \
    WinkFan


# pylint: disable=redefined-variable-type,too-many-branches
def build_device(device_state_as_json, api_interface):

    new_object = None

    # These objects all share the same base class: WinkDevice

    if "light_bulb_id" in device_state_as_json:
        new_object = WinkBulb(device_state_as_json, api_interface)
    elif "sensor_pod_id" in device_state_as_json:
        new_object = WinkSensorPod(device_state_as_json, api_interface)
    elif "binary_switch_id" in device_state_as_json:
        new_object = WinkBinarySwitch(device_state_as_json, api_interface)
    elif "outlet_id" in device_state_as_json:
        new_object = WinkPowerStripOutlet(device_state_as_json, api_interface)
    elif "lock_id" in device_state_as_json:
        new_object = WinkLock(device_state_as_json, api_interface)
    elif "eggtray_id" in device_state_as_json:
        new_object = WinkEggTray(device_state_as_json, api_interface)
    elif "garage_door_id" in device_state_as_json:
        new_object = WinkGarageDoor(device_state_as_json, api_interface)
    elif "shade_id" in device_state_as_json:
        new_object = WinkShade(device_state_as_json, api_interface)
    elif "siren_id" in device_state_as_json:
        new_object = WinkSiren(device_state_as_json, api_interface)
    elif "key_id" in device_state_as_json:
        new_object = WinkKey(device_state_as_json, api_interface)
    elif "thermostat_id" in device_state_as_json:
        new_object = WinkThermostat(device_state_as_json, api_interface)
    elif "fan_id" in device_state_as_json:
        new_object = WinkFan(device_state_as_json, api_interface)

    return new_object or WinkDevice(device_state_as_json, api_interface)
