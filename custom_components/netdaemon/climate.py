"""Climate platform for NetDaemon."""
from typing import TYPE_CHECKING

from homeassistant.components.climate import (
    ClimateEntity,
    SUPPORT_AUX_HEAT,
    SUPPORT_FAN_MODE,
    SUPPORT_PRESET_MODE,
    SUPPORT_SWING_MODE,
    SUPPORT_TARGET_HUMIDITY,
    SUPPORT_TARGET_TEMPERATURE,
    SUPPORT_TARGET_TEMPERATURE_RANGE,
)

from .const import (
    ATTR_CLIENT,
    ATTR_COORDINATOR,
    ATTR_ENTITY_ID,
    ATTR_STATE,
    DOMAIN,
    LOGGER,
    PLATFORM_CLIMATE,
    STATE_ON_VALUES,
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
    """Setup switch platform."""
    client: "NetDaemonClient" = hass.data[DOMAIN][ATTR_CLIENT]
    coordinator: "DataUpdateCoordinator" = hass.data[DOMAIN][ATTR_COORDINATOR]

    climate_entities = []
    for entity in client.entities:
        if entity.split(".")[0] == PLATFORM_CLIMATE:
            LOGGER.debug("Adding %s", entity)
            climate_entities.append(
                NetDaemonClimateEntity(coordinator, entity.split(".")[1])
            )

    if climate_entities:
        async_add_devices(climate_entities)


class NetDaemonClimateEntity(NetDaemonEntity, ClimateEntity):
    """NetDaemon ClimateEntity class."""

    # @property
    # def is_on(self):
    #     """Return the state of the switch."""
    #     state = str(self._coordinator.data[self.entity_id][ATTR_STATE]).lower()
    #     return state in STATE_ON_VALUES

    # async def async_turn_on(self, **kwargs):
    #     """Turn the device on."""
    #     await self._async_toggle()

    # async def async_turn_off(self, **kwargs):
    #     """Turn the device off."""
    #     await self._async_toggle()

    # async def _async_toggle(self) -> None:
    #     """Toggle the switch entity."""
    #     current = self._coordinator.data[self.entity_id][ATTR_STATE]
    #     await self.hass.data[DOMAIN][ATTR_CLIENT].entity_update(
    #         {ATTR_ENTITY_ID: self.entity_id, ATTR_STATE: not current}
    #     )
    #     self.async_write_ha_state()
