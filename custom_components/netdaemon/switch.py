"""Switch platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_ICON,
    ATTR_STATE,
    ATTR_UNIT,
    DOMAIN,
    LOGGER,
    PLATFORM_SWITCH,
)
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup switch platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN]

    switches = []
    for entity in client.entities:
        if entity.split(".")[0] == PLATFORM_SWITCH:
            LOGGER.debug("Adding %s", entity)
            switches.append(
                NetDaemonSwitch(
                    entity.split(".")[1],
                    client.entities[entity].get(ATTR_STATE, False),
                    client.entities[entity].get(ATTR_ICON),
                    client.entities[entity].get(ATTR_ATTRIBUTES, {}),
                    client.entities[entity].get(ATTR_UNIT),
                )
            )

    if switches:
        async_add_devices(switches)


class NetDaemonSwitch(NetDaemonEntity, SwitchEntity):
    """NetDaemon Switch class."""

    @property
    def is_on(self):
        """Return the state of the switch."""
        return self._state

    def turn_on(self, **kwargs):
        """Turn the device on."""
        self._toggle()

    def turn_off(self, **kwargs):
        """Turn the device off."""
        self._toggle()

    def _toggle(self) -> None:
        """Toggle the switch entity."""
        self._state = not self._state
        self.async_write_ha_state()
