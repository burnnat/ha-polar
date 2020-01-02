"""The Polar component."""
__version__ = '0.0.2'

import logging

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
import homeassistant.helpers.config_validation as cv

from .const import (
    DOMAIN, CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_UNIT_SYSTEM,
    CONF_MONITORED_RESOURCES, CONF_DAILY_ACTIVITY, CONF_TRAINING_DATA,
    CONF_PHYSICAL_INFO, RESOURCE_NAMES)

_LOGGER = logging.getLogger(__name__)

CONFIG_SCHEMA = vol.Schema(
    {
        DOMAIN: {
            CONF_CLIENT_ID: cv.string,
            CONF_CLIENT_SECRET: cv.string,
            CONF_UNIT_SYSTEM: cv.unit_system,
            CONF_MONITORED_RESOURCES: {
                CONF_DAILY_ACTIVITY: vol.All(
                    cv.ensure_list,
                    [vol.In(RESOURCE_NAMES[CONF_DAILY_ACTIVITY])]),
                CONF_TRAINING_DATA: vol.All(
                    cv.ensure_list,
                    [vol.In(RESOURCE_NAMES[CONF_TRAINING_DATA])]),
                CONF_PHYSICAL_INFO: vol.All(
                    cv.ensure_list,
                    [vol.In(RESOURCE_NAMES[CONF_PHYSICAL_INFO])])
            }
        }
    },
    extra=vol.ALLOW_EXTRA
)

async def async_setup(hass, config):
    """Set up the Polar component."""
    conf = config.get(DOMAIN)

    hass.data[DOMAIN] = conf or {}

    if conf is not None:
        _LOGGER.debug('Setting up Polar config flow from configuration data')

        hass.async_create_task(
            hass.config_entries.flow.async_init(
                DOMAIN, context={"source": config_entries.SOURCE_IMPORT}, data=conf
            )
        )

    return True


async def async_setup_entry(hass, entry):
    """Set up Polar integration from a config entry."""
    _LOGGER.debug('Setting up Polar integration')

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, SENSOR_DOMAIN)
    )

    return True


async def async_unload_entry(hass, entry):
    """Unload a config entry."""
    _LOGGER.debug('Unloading Polar integration')

    await hass.config_entries.async_forward_entry_unload(entry, SENSOR_DOMAIN)

    return True
