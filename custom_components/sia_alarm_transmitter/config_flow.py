"""Configuration flow for SIA Alarm Transmitter."""
import voluptuous as vol
import homeassistant.helpers.config_validation as cv
from homeassistant.config_entries import ConfigFlow, OptionsFlow
from homeassistant.core import callback
from .const import DOMAIN, DEFAULT_PORT

class SIAConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle SIA Transmitter configuration."""
    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle user configuration."""
        errors = {}

        if user_input is not None:
            # Optional: Add connection validation
            return self.async_create_entry(
                title=f"SIA Alarm: {user_input['primary_host']}",
                data=user_input
            )

        # Configuration form schema with TLS parameters
        data_schema = vol.Schema({
            vol.Required("primary_host"): str,
            vol.Required("primary_port", default=DEFAULT_PORT): int,
            vol.Optional("backup_host"): str,
            vol.Optional("backup_port", default=DEFAULT_PORT): int,
            vol.Required("account_code"): str,
            vol.Optional("protocol_number", default='6678'): str,
            vol.Optional("station_id", default='0000'): str,
            vol.Optional("subscriber_id", default='0000'): str,
        })

        return self.async_show_form(
            step_id="user",
            data_schema=data_schema,
            errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Create the options flow."""
        return SIAOptionsFlow(config_entry)

class SIAOptionsFlow(OptionsFlow):
    """Options flow for SIA Transmitter."""
    def __init__(self, config_entry):
        """Initialize options flow."""
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage Transmitter options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Optional(
                    "retry_attempts", 
                    default=self.config_entry.options.get("retry_attempts", 2)
                ): int,
                vol.Optional(
                    "timeout", 
                    default=self.config_entry.options.get("timeout", 10)
                ): int,
            })
        )
