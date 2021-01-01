"""NetDaemon class."""
from typing import TYPE_CHECKING, List

from homeassistant.helpers import entity_registry
from homeassistant.helpers.storage import Store
from homeassistant.helpers.json import JSONEncoder

from .const import LOGGER, STORAGE_VERSION

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant


class NetDaemonClient:
    """NetDaemon class."""

    def __init__(self, hass: "HomeAssistant") -> None:
        """Initialize the NetDaemon class."""
        self.hass = hass
        self._entities: dict = {}
        self._store = Store(hass, STORAGE_VERSION, "netdaemon", encoder=JSONEncoder)

    @property
    def entities(self) -> List[str]:
        """Return a list of entities."""
        return self._entities

    async def load(self) -> None:
        """Load stored data."""
        restored = await self._store.async_load()
        self._entities = restored if restored else {}

    async def clear_storage(self) -> None:
        """Clear storage."""
        await self._store.async_remove()

    async def entity_create(self, data) -> None:
        """Create an entity."""
        LOGGER.info("Creating entity %s", data)
        if data["entity_id"] in self._entities:
            del self._entities[data["entity_id"]]

        self._entities[data["entity_id"]] = {
            "state": data.get("state"),
            "icon": data.get("icon"),
            "unit": data.get("unit"),
            "attributes": data.get("attributes", {}),
        }
        await self._store.async_save(self._entities)

    async def entity_update(self, data) -> None:
        """Update an entity."""
        if data["entity_id"] not in self._entities:
            LOGGER.error("Entity ID %s is not managed by the netdaemon integration")
            return False
        await self.entity_create(data)
        await self._store.async_save(self._entities)
        return True

    async def entity_remove(self, data) -> None:
        """Remove an entity."""
        if data["entity_id"] not in self._entities:
            LOGGER.error("Entity ID %s is not managed by the netdaemon integration")
            return False
        LOGGER.info("Removing entity %s", data)
        del self._entities[data["entity_id"]]
        registry = await entity_registry.async_get_registry(self.hass)
        if data["entity_id"] in registry.entities:
            registry.async_remove(data["entity_id"])
        await self._store.async_save(self._entities)
