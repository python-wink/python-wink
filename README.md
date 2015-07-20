Python Wink API
---------------

### Script works but no longer maintained. Looking for maintainers.

Python implementation of the Wink API supporting switches, light bulbs and sensors.

Script by [John McLaughlin](https://github.com/loghound).

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
    switch.setState(!switch.state())
```
