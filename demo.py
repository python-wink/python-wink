import pywink
pywink.set_bearer_token('d7cbda4bf96789e3270c332ebf6a6d5c')

for switch in pywink.get_bulbs():
    print("Toggling {} to {}".format(switch.name(), switch.state()))
    # switch.set_state(not switch.state())
