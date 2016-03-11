from pywink.devices.base import WinkDevice
from pywink.devices.sensors import WinkSensorPod
from pywink.devices.standard import WinkBulb, WinkBinarySwitch, WinkPowerStripOutlet, WinkLock, \
    WinkEggTray, WinkGarageDoor, WinkSiren


def build_device(device_state_as_json, api_interface):

    assert device_state_as_json is not None

    new_object = None

    # pylint: disable=redefined-variable-type
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
    elif "siren_id" in device_state_as_json:
        new_object = WinkSiren(device_state_as_json, api_interface)

    return new_object or WinkDevice(device_state_as_json, api_interface)
