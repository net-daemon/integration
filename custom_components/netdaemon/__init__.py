"""NetDaemon integration."""
import asyncio
from typing import TYPE_CHECKING

from homeassistant.exceptions import ConfigEntryNotReady

from .const import DOMAIN, ATTR_CLASS, ATTR_METHOD, LOGGER, PLATFORMS
from .client import NetDaemonClient


if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.config_entries import ConfigEntry


async def async_setup(_hass: "HomeAssistant", _config: dict) -> bool:
    """Set up this integration using yaml."""
    return True


async def async_setup_entry(hass: "HomeAssistant", config_entry: "ConfigEntry") -> bool:
    """Set up this integration using UI."""
    client = NetDaemonClient(hass)
    hass.data[DOMAIN] = client

    # Load stored data from .storage/netdaemon
    await client.load()

    # Services
    async def handle_register_service(call):
        """Register custom services."""
        daemon_class = call.data.get(ATTR_CLASS, "no class provided")
        daemon_method = call.data.get(ATTR_METHOD, "no method provided")

        LOGGER.info("Register service %s_%s", daemon_class, daemon_method)
        hass.services.async_register(
            DOMAIN, f"{daemon_class}_{daemon_method}", netdaemon_noop
        )

    async def netdaemon_noop(_call):
        """Do nothing for now, the netdaemon subscribes to this service."""

    async def entity_create(call):
        """Create an entity."""
        entity_id = call.data.get("entity_id")
        if not entity_id:
            LOGGER.error("No 'entity_id' for service entity_create")
        if "." not in entity_id:
            LOGGER.error(
                "%s is not a valid entity ID for service entity_create", entity_id
            )
        if entity_id.split(".")[0] not in PLATFORMS:
            LOGGER.error(
                "%s is not a valid platform (%s) for service entity_create",
                entity_id.split(".")[0],
                PLATFORMS,
            )

        await client.entity_create(call.data)
        await async_reload_entry(hass, config_entry)

    async def entity_update(call):
        """Create an entity."""
        entity_id = call.data.get("entity_id")
        if not entity_id:
            LOGGER.error("No 'entity_id' for service entity_create")
        if "." not in entity_id:
            LOGGER.error(
                "%s is not a valid entity ID for service entity_create", entity_id
            )
        if entity_id.split(".")[0] not in PLATFORMS:
            LOGGER.error(
                "%s is not a valid platform (%s) for service entity_create",
                entity_id.split(".")[0],
                PLATFORMS,
            )

        if await client.entity_update(call.data):
            await async_reload_entry(hass, config_entry)

    async def entity_remove(call):
        """Create an entity."""
        entity_id = call.data.get("entity_id")
        if not entity_id:
            LOGGER.error("No 'entity_id' for service entity_create")
        if "." not in entity_id:
            LOGGER.error(
                "%s is not a valid entity ID for service entity_create", entity_id
            )
        if entity_id.split(".")[0] not in PLATFORMS:
            LOGGER.error(
                "%s is not a valid platform (%s) for service entity_create",
                entity_id.split(".")[0],
                PLATFORMS,
            )
        await client.entity_remove(call.data)

    hass.services.async_register(DOMAIN, "register_service", handle_register_service)
    hass.services.async_register(DOMAIN, "reload_apps", netdaemon_noop)
    hass.services.async_register(DOMAIN, "entity_create", entity_create)
    hass.services.async_register(DOMAIN, "entity_update", entity_update)
    hass.services.async_register(DOMAIN, "entity_remove", entity_remove)

    # Platforms
    for platform in PLATFORMS:
        LOGGER.debug("Adding platfrom %s", platform)
        hass.async_add_job(
            hass.config_entries.async_forward_entry_setup(config_entry, platform)
        )

    config_entry.add_update_listener(async_reload_entry)
    return True


async def async_unload_entry(hass: "HomeAssistant", entry: "ConfigEntry") -> bool:
    """Handle removal of an entry."""
    unloaded = all(
        await asyncio.gather(
            *[
                hass.config_entries.async_forward_entry_unload(entry, platform)
                for platform in PLATFORMS
            ]
        )
    )
    if unloaded:
        del hass.data[DOMAIN]

    return unloaded


async def async_remove_entry(
    hass: "HomeAssistant", _config_entry: "ConfigEntry"
) -> None:
    """Handle removal of an entry."""
    await NetDaemonClient(hass).clear_storage()


async def async_reload_entry(
    hass: "HomeAssistant", config_entry: "ConfigEntry"
) -> None:
    """Reload the config entry."""
    await async_unload_entry(hass, config_entry)
    await async_setup_entry(hass, config_entry)
