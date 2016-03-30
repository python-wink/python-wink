def is_desired_state_reached(wink_device_state):
    """
    :type wink_device: dict
    """
    desired_state = wink_device_state.get('desired_state', {})
    for name, value in desired_state.items():
        if value != wink_device_state.get(name):
            return False

    return True
