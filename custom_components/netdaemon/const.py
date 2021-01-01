"""Constants for NetDaemon."""
import logging

LOGGER: logging.Logger = logging.getLogger(__package__)

VERSION = "main"
DOMAIN = "netdaemon"
NAME = "NetDaemon"
MINIMUM_HA_VERSION = "2020.12.0"
STORAGE_VERSION = "1"

ND_ID = "86ec6a70-b2b8-427d-8fcf-3f14331dddd7"

ATTR_CLASS = "class"
ATTR_METHOD = "method"

PLATFORMS = ["binary_sensor", "sensor", "switch"]

STARTUP = f"""
-------------------------------------------------------------------
NetDaemon
Version: {VERSION}
This is a custom integration
If you have any issues with this you need to open an issue here:
https://github.com/hacs/integration/issues
-------------------------------------------------------------------
"""