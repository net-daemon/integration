"""Switch platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.switch import SwitchEntity

from .const import DOMAIN, LOGGER
from .entity import NetDaemonEntity

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry

    from .client import NetDaemonClient


async def async_setup_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry", async_add_devices
) -> None:
    """Setup switch platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN]

    switches = []
    for entity in client.entities:
        if entity.split(".")[0] == "switch":
            LOGGER.debug("Adding %s", entity)
            switches.append(
                NetDaemonSwitch(
                    entity.split(".")[1],
                    client.entities[entity].get("state", False),
                    client.entities[entity].get("icon"),
                    client.entities[entity].get("attributes", {}),
                    client.entities[entity].get("unit"),
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
