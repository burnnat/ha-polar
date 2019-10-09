import datetime
import isodate

DOMAIN = 'polar'

CONF_CLIENT_ID = 'client_id'
CONF_CLIENT_SECRET = 'client_secret'
CONF_UNIT_SYSTEM = 'unit_system'
CONF_USER_ID = 'user_id'
CONF_ACCESS_TOKEN = 'access_token'
CONF_MONITORED_RESOURCES = 'monitored_resources'
CONF_DAILY_ACTIVITY = 'daily_activity'
CONF_TRAINING_DATA = 'training_data'
CONF_PHYSICAL_INFO = 'physical_info'

AUTH_CALLBACK_NAME = "api:polar_auth"
AUTH_CALLBACK_PATH = "/api/polar_auth"

SYSTEM_IMPERIAL = 'imperial'
SYSTEM_METRIC = 'metric'

class PolarEndpointType:
    """Base class for modeling Polar endpoints."""

    def __init__(self, name, result_name, timestamp_name, list_method, get_method):
        self.name = name
        self.result_name = result_name
        self.timestamp_name = timestamp_name
        self.list_method = list_method
        self.get_method = get_method

ENDPOINTS = {
    CONF_DAILY_ACTIVITY: PolarEndpointType(
        'daily_activity',
        'activity-log',
        'created',
        'list_activities',
        'get_activity_summary'),
    CONF_TRAINING_DATA: PolarEndpointType(
        'training_data',
        'exercises',
        'start-time',
        'list_exercises',
        'get_exercise_summary'),
    CONF_PHYSICAL_INFO: PolarEndpointType(
        'physical_info',
        'physical-informations',
        'created',
        'list_physical_infos',
        'get_physical_info')}

class PolarResource:
    """Base class for modeling Polar data."""

    def __init__(self, name, friendly_name, units, icon):
        """Constructor."""
        self.name = name
        self.friendly_name = friendly_name
        self.units = units
        self.icon = icon

class SimpleUnit:
    """Simple class for units that are the same under both imperial and metric systems"""

    def __init__(self, unit):
        self._unit = unit

    def unit(self, system):
        return self._unit

    def parse(self, raw, system):
        return raw


class ScaledUnit:
    def __init__(self, units, conversions):
        self._units = units
        self._conversions = conversions

    def unit(self, system):
        return self._units[system]

    def parse(self, raw, system):
        return raw / self._conversions[system]

class TimestampUnit:
    def unit(self, system):
        return None

    def parse(self, raw, system):
        value = datetime.datetime.fromisoformat(raw)
        return value

class DurationUnit:
    def unit(self, system):
        return 'mins'

    def parse(self, raw, system):
        value = isodate.parse_duration(raw)
        return value.total_seconds() / 60

RESOURCES = {
    CONF_DAILY_ACTIVITY: [
        PolarResource(
            'calories',
            'Calories',
            SimpleUnit('kcal'),
            'mdi:fire'),
        PolarResource(
            'active-calories',
            'Active Calories',
            SimpleUnit('kcal'),
            'mdi:fire'),
        PolarResource(
            'duration',
            'Duration',
            DurationUnit(),
            'mdi:clock'),
        PolarResource(
            'active-steps',
            'Active Steps',
            SimpleUnit('steps'),
            'mdi:walk')],
    CONF_TRAINING_DATA: [
        PolarResource(
            'device',
            'Device',
            SimpleUnit(None),
            None),
        PolarResource(
            'start-time',
            'Start Time',
            TimestampUnit(),
            'mdi:clock'),
        PolarResource(
            'duration',
            'Duration',
            DurationUnit(),
            'mdi:clock'),
        PolarResource(
            'calories',
            'Calories',
            SimpleUnit('kcal'),
            'mdi:fire'),
        PolarResource(
            'distance',
            'Distance',
            ScaledUnit(
                { SYSTEM_IMPERIAL: 'mi', SYSTEM_METRIC: 'km' },
                { SYSTEM_IMPERIAL: 1609.34, SYSTEM_METRIC: 1000 }),
            'mdi:map-marker'),
        PolarResource(
            'heart-rate/average',
            'Average Heart Rate',
            SimpleUnit('bpm'),
            'mdi:heart-pulse'),
        PolarResource(
            'heart-rate/maximum',
            'Maximum Heart Rate',
            SimpleUnit('bpm'),
            'mdi:heart-pulse'),
        PolarResource(
            'training-load',
            'Training Load',
            SimpleUnit(None),
            'mdi:run'),
        PolarResource(
            'sport',
            'Sport',
            SimpleUnit(None),
            None),
        PolarResource(
            'has-route',
            'Has Route',
            SimpleUnit(None),
            None),
        PolarResource(
            'club-id',
            'Club ID',
            SimpleUnit(None),
            None),
        PolarResource(
            'club-name',
            'Club Name',
            SimpleUnit(None),
            None),
        PolarResource(
            'detailed-sport-info',
            'Detailed Sport',
            SimpleUnit(None),
            None)],
    CONF_PHYSICAL_INFO: [
        PolarResource(
            'weight',
            'Weight',
            ScaledUnit(
                { SYSTEM_IMPERIAL: 'lbs', SYSTEM_METRIC: 'kg' },
                { SYSTEM_IMPERIAL: 0.453592, SYSTEM_METRIC: 1 }),
            'mdi:human'),
        PolarResource(
            'height',
            'Height',
            ScaledUnit(
                { SYSTEM_IMPERIAL: 'ft', SYSTEM_METRIC: 'm' },
                { SYSTEM_IMPERIAL: 30.48, SYSTEM_METRIC: 100 }),
            'mdi:human'),
        PolarResource(
            'maximum-heart-rate',
            'Maximum Heart Rate',
            SimpleUnit('bpm'),
            'mdi:heart-pulse'),
        PolarResource(
            'resting-heart-rate',
            'Resting Heart Rate',
            SimpleUnit('bpm'),
            'mdi:heart-pulse'),
        PolarResource(
            'aerobic-threshold',
            'Aerobic Threshold',
            SimpleUnit('bpm'),
            None),
        PolarResource(
            'anaerobic-threshold',
            'Anaerobic Threshold',
            SimpleUnit('bpm'),
            None),
        PolarResource(
            'vo2-max',
            'VO2 Max',
            SimpleUnit('L/min'),
            None)]}

RESOURCES_BY_NAME = {
    endpoint: { resource.name: resource for resource in resources }
        for endpoint, resources in RESOURCES.items() }

RESOURCE_NAMES = {
    endpoint: resources.keys()
        for endpoint, resources in RESOURCES_BY_NAME.items() }