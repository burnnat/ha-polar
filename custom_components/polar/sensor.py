"""Support for HDHomeRun devices."""
import logging

from accesslink import AccessLink

from homeassistant.helpers.restore_state import RestoreEntity

from .const import (
    DOMAIN, CONF_CLIENT_ID, CONF_CLIENT_SECRET, CONF_USER_ID,
    CONF_ACCESS_TOKEN, CONF_MONITORED_RESOURCES, CONF_DAILY_ACTIVITY,
    CONF_TRAINING_DATA, CONF_PHYSICAL_INFO, ENDPOINTS, RESOURCES_BY_NAME)

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass, entry, async_add_entities):
    """Set up Polar from a config entry."""
    resources_by_endpoint = hass.data[DOMAIN].get(CONF_MONITORED_RESOURCES)

    accesslink = AccessLink(client_id=entry.data.get(CONF_CLIENT_ID),
                        client_secret=entry.data.get(CONF_CLIENT_SECRET))

    user_id = entry.data.get(CONF_USER_ID)
    access_token = entry.data.get(CONF_ACCESS_TOKEN)

    if resources_by_endpoint is not None:
        entities = []

        for endpoint_name, resources in resources_by_endpoint.items():
            _LOGGER.debug('Setting up Polar entities for endpoint: %s', endpoint_name)

            endpoint = PolarEndpoint(accesslink, ENDPOINTS[endpoint_name], user_id, access_token)
            add_resource_entities(entities, endpoint, resources)

        async_add_entities(entities, update_before_add=False)

    return True

def add_resource_entities(entities, endpoint, resources):
    endpoint_name = endpoint.name
    master = None

    for resource_name in resources:
        resource = RESOURCES_BY_NAME[endpoint_name][resource_name]

        _LOGGER.debug('Setting up Polar sensor for resource: %s/%s', endpoint_name, resource_name)

        if master is None:
            _LOGGER.debug('Entity %s/%s is master sensor', endpoint_name, resource_name)
            sensor = PolarMasterSensor(endpoint, resource)
            master = sensor
        else:
            sensor = PolarSensor(endpoint, resource)
            master.add_child(sensor)
        
        entities.append(sensor)

class PolarEndpoint:
    """Wrapper class for standardizing calls to Polar endpoints."""

    def __init__(self, accesslink, endpoint_type, user_id, access_token):
        self._accesslink = accesslink
        self._endpoint = endpoint_type
        self._user_id = user_id
        self._access_token = access_token
        self._transaction = None

    @property
    def name(self):
        return self._endpoint.name

    def create_transaction(self):
        return getattr(self._accesslink, self._endpoint.name).create_transaction(self._user_id, self._access_token)

    def list_updates(self, transaction):
        result = getattr(transaction, self._endpoint.list_method)()
        return result[self._endpoint.result_name]

    def get_update(self, transaction, url):
        return getattr(transaction, self._endpoint.get_method)(url)

    def get_timestamp(self, data):
        return data[self._endpoint.timestamp_name]

class PolarSensor(RestoreEntity):
    """Representation of a sensor."""

    def __init__(self, endpoint, resource):
        """Initialize the sensor."""
        self._endpoint = endpoint
        self._resource = resource
        self._state = None

    @property
    def should_poll(self):
        return False

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

    async def async_update_from_raw(self, raw):
        item = raw
        keys = self._resource.name.split('/')

        for key in keys:
            item = item[key]

        _LOGGER.debug('Setting state for resource %s/%s: %s', self._endpoint.name, self._resource.name, item)
        self._state = item

        if not self.should_poll:
            _LOGGER.debug('Triggering state update for resource: %s/%s', self._endpoint.name, self._resource.name)
            await self.async_update_ha_state()

    async def async_added_to_hass(self):
        """Run when entity about to be added to hass."""
        await super().async_added_to_hass()
        if self._state is not None:
            return

        _LOGGER.debug('Restoring state for resource: %s/%s', self._endpoint.name, self._resource.name)
        previous = await self.async_get_last_state()

        if previous is not None:
            self._state = previous.state

class PolarMasterSensor(PolarSensor):
    """Master sensor to coordinate update transactions to an Accesslink endpoint."""

    def __init__(self, endpoint, resource):
        """Initialize the sensor."""
        super().__init__(endpoint, resource)
        self._children = []

    @property
    def should_poll(self):
        return True

    def add_child(self, child_entity):
        self._children.append(child_entity)

    async def async_update(self):
        """Update the sensor state."""
        _LOGGER.debug('Beginning update for master sensor: %s/%s', self._endpoint.name, self._resource.name)

        transaction = self._endpoint.create_transaction()

        if transaction is None:
            _LOGGER.debug('No updates available for endpoint %s', self._endpoint.name)
            return

        updates = self._endpoint.list_updates(transaction)

        if updates is not None:
            timestamp = None
            recent_update = None

            _LOGGER.debug('Found %d updates for endpoint %s', len(updates), self._endpoint.name)

            for url in updates:
                _LOGGER.debug('Reading update for URL: %s', url)
                data = self._endpoint.get_update(transaction, url)

                if timestamp is None or self._endpoint.get_timestamp(data) > timestamp:
                    recent_update = data

            _LOGGER.debug('Using most recent update: %s', recent_update)

            await self.async_update_from_raw(recent_update)

            for child in self._children:
                await child.async_update_from_raw(recent_update)

        transaction.commit()