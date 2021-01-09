"""Binary sensor platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.binary_sensor import BinarySensorEntity

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_CLIENT,
    ATTR_COORDINATOR,
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
    from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup binary sensor platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN][ATTR_CLIENT]
    coordinator: "DataUpdateCoordinator" = hass.data[DOMAIN][ATTR_COORDINATOR]

    binary_sensors = []
    for entity in client.entities:
        if entity.split(".")[0] == PLATFORM_BINARY_SENSOR:
            LOGGER.debug("Adding %s", entity)
            binary_sensors.append(
                NetDaemonBinarySensor(
                    coordinator,
                    entity.split(".")[1],
                    client.entities[entity].get(ATTR_ICON),
                    client.entities[entity].get(ATTR_ATTRIBUTES, {}),
                    client.entities[entity].get(ATTR_UNIT),
                )
            )

    if binary_sensors:
        async_add_devices(binary_sensors)


class NetDaemonBinarySensor(NetDaemonEntity, BinarySensorEntity):
    """NetDaemon Binary sensor class."""

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._coordinator.data[self.entity_id][ATTR_STATE]
