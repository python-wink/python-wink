Python Wink API
---------------

[![Join the chat at https://gitter.im/bradsk88/python-wink](https://badges.gitter.im/bradsk88/python-wink.svg)](https://gitter.im/bradsk88/python-wink?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) [![Build Status](https://travis-ci.org/bradsk88/python-wink.svg?branch=master)](https://travis-ci.org/bradsk88/python-wink)
[![Coverage Status](https://coveralls.io/repos/github/bradsk88/python-wink/badge.svg?branch=master)](https://coveralls.io/github/bradsk88/python-wink?branch=master)

_This script used to be part of Home Assistant. It has been extracted to fit
the goal of Home Assistant to not contain any device specific API implementations
but rely on open-source implementations of the API._

## Authentication

You will need a Wink API bearer token to communicate with the Wink server.

[Get yours using this web app.](https://winkbearertoken.appspot.com/)

## Example usage

```python
import pywink
pywink.set_bearer_token('YOUR_BEARER_TOKEN')

for switch in pywink.get_switches():
    print(switch.name(), switch.state())
    switch.set_state(!switch.state())
```
