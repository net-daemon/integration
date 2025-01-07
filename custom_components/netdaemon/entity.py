"""NetDaemon entity."""
from awesomeversion import AwesomeVersion
from homeassistant.const import __version__ as HA_VERSION
from homeassistant.core import callback
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
)

from .const import (
    ATTR_ATTRIBUTES,
    ATTR_ICON,
    ATTR_UNIT,
    DOMAIN,
    INTEGRATION_VERSION,
    NAME,
    ND_ID,
)


# class CoordinatorEntity(BaseCoordinatorEntity[_DataUpdateCoordinatorT]):
#     """A class for entities using DataUpdateCoordinator."""
#
#     def __init__(
#         self, coordinator: _DataUpdateCoordinatorT, context: Any = None
#     ) -> None:
#         """Create the entity with a DataUpdateCoordinator.
#
#         Passthrough to BaseCoordinatorEntity.
#
#         Necessary to bind TypeVar to correct scope.
#         """
#         super().__init__(coordinator, context)
#
#     @property
#     def available(self) -> bool:
#         """Return if entity is available."""
#         return self.coordinator.last_update_success
#
#     async def async_update(self) -> None:
#         """Update the entity.
#
#         Only used by the generic entity update service.
#         """
#         # Ignore manual update requests if the entity is disabled
#         if not self.enabled:
#             return
#
#         await self.coordinator.async_request_refresh()
class NetDaemonEntity(CoordinatorEntity):
    """NetDaemon entity."""

    def __init__(
        self,
        coordinator: DataUpdateCoordinator,
        name: str,
    ) -> None:
        """Initialize."""
        super().__init__(coordinator)
        self._coordinator = coordinator
        self._name = name

    def _data_point(self, key, default=None):
        if not self.entity_id:
            return None
        if not self._coordinator.data:
            return None
        if not self.available:
            return None

        return self._coordinator.data.get(self.entity_id, {}).get(key, default)

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{ND_ID}_{self._name}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._data_point(ATTR_UNIT)

    @property
    def available(self) -> bool:
        return super().available and self.entity_id in self._coordinator.data

    @property
    def icon(self):
        """Return the icon."""
        return self._data_point(ATTR_ICON)

    @property
    def device_info(self):
        """Return device information about NetDaemon."""
        info = {
            "identifiers": {(DOMAIN, ND_ID)},
            "name": NAME,
            "sw_version": INTEGRATION_VERSION,
            "manufacturer": "netdaemon.xyz",
        }
        # LEGACY can be removed when min HA version is 2021.12
        if AwesomeVersion(HA_VERSION) >= "2021.12.0b0":
            # pylint: disable=import-outside-toplevel
            from homeassistant.helpers.device_registry import DeviceEntryType

            info["entry_type"] = DeviceEntryType.SERVICE
        else:
            info["entry_type"] = "service"
        return info

    @property
    def extra_state_attributes(self):
        """Return attributes for the sensor."""
        attributes = {"integration": DOMAIN}
        for attr in self._data_point(ATTR_ATTRIBUTES, {}):
            attributes[attr] = self._coordinator.data[self.entity_id][ATTR_ATTRIBUTES][
                attr
            ]
        return attributes

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)
