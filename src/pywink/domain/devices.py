def is_desired_state_reached(wink_device_state):
    """
    :type wink_device: dict
    """
    desired_state = wink_device_state.get('desired_state', {})
    last_reading = wink_device_state.get('last_reading', {})
    if not last_reading.get('connection', True):
        return True
    for name, desired_value in desired_state.items():
        latest_value = last_reading.get(name)
        if desired_value != latest_value:
            return False

    return True
