"""Support for HDHomeRun devices."""
import logging

from accesslink import AccessLink

from homeassistant.helpers.restore_state import RestoreEntity

from .const import DOMAIN, CONF_MONITORED_RESOURCES, CONF_DAILY_ACTIVITY
    CONF_TRAINING_DATA, CONF_PHYSICAL_INFO, ENDPOINTS, RESOURCES

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Polar from a config entry."""
    resources_by_endpoint = hass.data[DOMAIN].get(CONF_MONITORED_RESOURCES)

    accesslink = AccessLink(client_id=entry.data.get(CLIENT_ID),
                        client_secret=entry.data.get(CLIENT_SECRET))

    entities = []

    for endpoint_name, resources in resources_by_endpoint.items():
        endpoint = PolarEndpoint(accesslink, ENDPOINTS[endpoint_name])
        add_resource_entities(entities, endpoint, resources)

    async_add_entities(entities, update_before_add=True)

    return True

def add_resource_entities(entities, endpoint, resources):
    master = None

    for resource in resources:
        if master is None:
            sensor = PolarSensor(endpoint, resource)
            master = sensor
        else:
            sensor = PolarSensor(None, resource)
            master.add_child(sensor)
        
        entities.append(sensor)

class PolarEndpoint:
    """Wrapper class for standardizing calls to Polar endpoints."""

    def __init__(self, accesslink, endpoint_type):
        self._accesslink = accesslink
        self._endpoint = endpoint_type
        self._transaction = None

    def create_transaction():
        return getattr(self._accesslink, self._endpoint.name).create_transaction()

    def list_updates(transaction):
        result = getattr(transaction, self._endpoint.list_method)()
        return result[self._endpoint.result_name]

    def get_update(transaction, url):
        return getattr(transaction, self._endpoint.get_method)(url)

    def get_timestamp(data):
        return data[self._endpoint.timestamp_name]

class PolarSensor(RestoreEntity):
    """Representation of a sensor."""

    def __init__(self, endpoint, resource):
        """Initialize the sensor."""
        self._master = endpoint is not None
        self._endpoint = endpoint
        self._resource = resource
        self._state = None

    async def async_update(self):
        self._state = None

    @property
    def should_poll(self):
        """If entity should be polled."""
        return self._master

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._resource.friendly_name

    @property
    def icon(self):
        """Return the icon for the sensor."""
        return self._resource.icon

    @property
    def state(self):
        """Return the state of the sensor."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._resource.units

    async def async_update(self):
        """Update the sensor state."""
        transaction = self._endpoint.create_transaction()

        updates = self._endpoint.list_updates(transaction)

        if updates is not None:
            timestamp = None
            recent_update = None

            for url in updates:
                data = self._endpoint.get_update(transaction, url)

                if timestamp is None or self._endpoint.get_timestamp(data) > timestamp:
                    recent_update = data

            await self.async_update_from_raw(recent_update)
            # update child sensors here too...

        transaction.commit()

    async def async_update_from_raw(self, raw):
        item = raw
        keys = self._endpoint.name.split('/')

        for key in keys:
            item = item[key]

        self._state = item

        if not self._master:
            await self.async_update_ha_state()

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        if self._state is not None:
            return

        self._state = await self.async_get_last_state()