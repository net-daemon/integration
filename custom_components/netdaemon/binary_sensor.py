"""Binary sensor platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_ICON,
    ATTR_STATE,
    ATTR_UNIT,
    DOMAIN,
    LOGGER,
    PLATFORM_BINARY_SENSOR,
)
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup binary sensor platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN]

    switches = []
    for entity in client.entities:
        if entity.split(".")[0] == PLATFORM_BINARY_SENSOR:
            LOGGER.debug("Adding %s", entity)
            switches.append(
                NetDaemonBinarySensor(
                    entity.split(".")[1],
                    client.entities[entity].get(ATTR_STATE, False),
                    client.entities[entity].get(ATTR_ICON),
                    client.entities[entity].get(ATTR_ATTRIBUTES, {}),
                    client.entities[entity].get(ATTR_UNIT),
                )
            )

    if switches:
        async_add_devices(switches)


class NetDaemonBinarySensor(NetDaemonEntity, BinarySensorEntity):
    """NetDaemon Binary sensor class."""

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state
