"""Configflow for the NetDaemon integration."""
import voluptuous as vol

from awesomeversion import AwesomeVersion

from homeassistant import config_entries
from homeassistant.const import __version__ as HAVERSION

from .const import DOMAIN, MINIMUM_HA_VERSION


class HacsFlowHandler(config_entries.ConfigFlow, domain=DOMAIN):
    """Config flow for HACS."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL

    def __init__(self):
        """Initialize."""
        self._errors = {}

    async def async_step_user(self, user_input):
        """Handle a flow initialized by the user."""
        self._errors = {}
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")
        if self.hass.data.get(DOMAIN):
            return self.async_abort(reason="single_instance_allowed")

        if user_input:
            if [x for x in user_input if not user_input[x] and x.startswith("acc_")]:
                self._errors["base"] = "acc"
                return await self._show_accowledge_form(user_input)

            return self.async_create_entry(title="", data={})

        return await self._show_accowledge_form(user_input)

    async def _show_accowledge_form(self, user_input):
        """Show the configuration form to edit location data."""
        if not user_input:
            user_input = {}

        if AwesomeVersion(HAVERSION) < MINIMUM_HA_VERSION:
            return self.async_abort(
                reason="min_ha_version",
                description_placeholders={"version": MINIMUM_HA_VERSION},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        "acc_issues", default=user_input.get("acc_issues", False)
                    ): bool,
                    vol.Required(
                        "acc_netdaemon", default=user_input.get("acc_netdaemon", False)
                    ): bool,
                    vol.Required(
                        "acc_disable", default=user_input.get("acc_disable", False)
                    ): bool,
                }
            ),
            errors=self._errors,
        )
