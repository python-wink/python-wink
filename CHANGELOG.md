# Change Log

## 0.5.0 
- Major bug fix.  Methods like `get_bulbs` were always returning empty lists.

## 0.4.3
- Added better error handling for API authorization problems.

## 0.4.2
- Added init method for WinkSiren

## 0.4.1
- Treating offline binary switches as if they have a powered state of false

## 0.4.0
- Removed API responses from docstring and moved into unit tests.
- Refactored __init__.py to support easier unit testing

## 0.3.3
- Added init method for Wink Power strip

## 0.3.2
- Added init method for WinkGarageDoor

## 0.3.1.1
- Changed mock to test-only dependency

## 0.3.1
- Added init method for WinkEggTray

## 0.3.0 
- Breaking change: Renamed classes to satisfy pylint

## 0.2.1
- Added ability to change color via setState
- Added ability to request color from wink_bulb object

## 0.2.0
- Initial work by balloob, ryanturner, and miniconfig
