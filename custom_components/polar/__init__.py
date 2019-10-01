"""The Polar component."""
__version__ = '0.0.1'

import logging

import voluptuous as vol
import homeassistant.helpers.config_validation as cv

from homeassistant import config_entries
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from .const import DOMAIN, CONF_CLIENT_ID, CONF_CLIENT_SECRET

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            CONF_CLIENT_ID: cv.string,
            CONF_CLIENT_SECRET: cv.string
        }
    },
    extra=vol.ALLOW_EXTRA
)

async def async_setup(hass, config):
    """Set up the Polar component."""
    conf = config.get(DOMAIN)

    _LOGGER.debug('Setting up Polar component with config data: ' + str(conf))

    hass.data[DOMAIN] = conf or {}

    if conf is not None:
        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data=conf
            )
        )

    return True


async def async_setup_entry(hass, entry):
    """Set up Polar integration from a config entry."""
    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, SENSOR_DOMAIN)
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    await hass.config_entries.async_forward_entry_unload(entry, SENSOR_DOMAIN)

    return True
