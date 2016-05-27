<img align="left" src="https://cloud.githubusercontent.com/assets/2147630/15595400/f5d7f8bc-237b-11e6-95b8-bb0353728e51.png"> Python Wink API

[![Join the chat at https://gitter.im/python-wink/python-wink](https://badges.gitter.im/python-wink/python-wink.svg)](https://gitter.im/bradsk88/python-wink?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Build Status](https://travis-ci.org/python-wink/python-wink.svg?branch=master)](https://travis-ci.org/python-wink/python-wink)
[![Coverage Status](https://coveralls.io/repos/github/python-wink/python-wink/badge.svg?branch=master)](https://coveralls.io/github/python-wink/python-wink?branch=master)

_This script used to be part of Home Assistant. It has been extracted to fit
the goal of Home Assistant to not contain any device specific API implementations
but rely on open-source implementations of the API._

## Example usage

```python
import pywink
pywink.set_bearer_token('YOUR_BEARER_TOKEN')

for switch in pywink.get_switches():
    print(switch.name(), switch.state())
    switch.set_state(not switch.state())
```
