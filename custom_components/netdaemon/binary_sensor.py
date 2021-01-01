"""Binary sensor platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import DOMAIN, LOGGER
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup binary sensor platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN]

    switches = []
    for entity in client.entities:
        if entity.split(".")[0] == "binary_sensor":
            LOGGER.debug("Adding %s", entity)
            switches.append(
                NetDaemonBinarySensor(
                    entity.split(".")[1],
                    client.entities[entity].get("state", False),
                    client.entities[entity].get("icon"),
                    client.entities[entity].get("attributes", {}),
                    client.entities[entity].get("unit"),
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
