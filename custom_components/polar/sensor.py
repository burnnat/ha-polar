"""Support for HDHomeRun devices."""
import logging

from hdhr.adapter import HdhrUtility, HdhrDeviceQuery

from homeassistant.components.sensor import DOMAIN as SENSOR_DOMAIN
from homeassistant.helpers.entity import Entity

from .const import DOMAIN, CONF_HOST

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up Polar from a config entry."""
    hosts = hass.data[DOMAIN].get(SENSOR_DOMAIN)
    devices = []

    async_add_entities(entities, update_before_add=True)

    return True

class PolarSensor(Entity):
    """Representation of a sensor."""

    def __init__(self):
        """Initialize the sensor."""
        self._name = 'Polar'
        self._unit_of_measurement = 'lbs'
        self._state = None

    async def async_update(self):
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement