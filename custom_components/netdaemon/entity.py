"""NetDaemon entity."""
from homeassistant.core import callback
from homeassistant.helpers.entity import Entity

from .const import INTEGRATION_VERSION, ND_ID, NAME, DOMAIN


class NetDaemonEntity(Entity):
    """NetDaemon entity."""

    def __init__(
        self, name: str, state: str, icon: str, attributes: dict, unit: str
    ) -> None:
        """Initialize."""
        self._name = name
        self._state = state
        self._icon = icon
        self._attributes = attributes
        self._unit = unit

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def should_poll(self):
        """No polling needed."""
        return False

    @property
    def unique_id(self):
        """Return a unique ID to use for this sensor."""
        return f"{ND_ID}_{self._name}"

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement."""
        return self._unit

    @property
    def icon(self):
        """Return the icon."""
        return self._icon

    @property
    def device_info(self):
        """Return device information about NetDaemon."""
        return {
            "identifiers": {(DOMAIN, ND_ID)},
            "name": NAME,
            "sw_version": INTEGRATION_VERSION,
            "manufacturer": "netdaemon.xyz",
            "entry_type": "service",
        }

    @property
    def device_state_attributes(self):
        """Return attributes for the sensor."""
        attributes = {"integration": DOMAIN}
        if self._attributes:
            for attr in self._attributes:
                attributes[attr] = self._attributes[attr]
        return attributes

    @callback
    def _schedule_immediate_update(self):
        self.async_schedule_update_ha_state(True)
