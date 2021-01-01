"""Sensor platform for NetDaemon."""
from typing import TYPE_CHECKING

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_ICON,
    ATTR_STATE,
    ATTR_UNIT,
    DOMAIN,
    LOGGER,
    PLATFORM_SENSOR,
)
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup sensor platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN]

    sensors = []
    for entity in client.entities:
        if entity.split(".")[0] == PLATFORM_SENSOR:
            LOGGER.debug("Adding %s", entity)
            sensors.append(
                NetDaemonSensor(
                    entity.split(".")[1],
                    client.entities[entity].get(ATTR_STATE, False),
                    client.entities[entity].get(ATTR_ICON),
                    client.entities[entity].get(ATTR_ATTRIBUTES, {}),
                    client.entities[entity].get(ATTR_UNIT),
                )
            )

    if sensors:
        async_add_devices(sensors)


class NetDaemonSensor(NetDaemonEntity):
    """NetDaemon Sensor class."""

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state
