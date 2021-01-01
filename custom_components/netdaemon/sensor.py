"""Sensor platform for NetDaemon."""
from typing import TYPE_CHECKING
from .const import DOMAIN, LOGGER
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup sensor platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN]

    sensors = []
    for entity in client.entities:
        if entity.split(".")[0] == "sensor":
            LOGGER.debug("Adding %s", entity)
            sensors.append(
                NetDaemonSensor(
                    entity.split(".")[1],
                    client.entities[entity].get("state"),
                    client.entities[entity].get("icon"),
                    client.entities[entity].get("attributes", {}),
                    client.entities[entity].get("unit"),
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
