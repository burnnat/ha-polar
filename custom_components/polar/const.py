DOMAIN = 'polar'

CONF_CLIENT_ID = 'client_id'
CONF_CLIENT_SECRET = 'client_secret'
CONF_USER_ID = 'user_id'
CONF_ACCESS_TOKEN = 'access_token'
CONF_MONITORED_RESOURCES = 'monitored_resources'
CONF_DAILY_ACTIVITY = 'daily_activity'
CONF_TRAINING_DATA = 'training_data'
CONF_PHYSICAL_INFO = 'physical_info'

AUTH_CALLBACK_NAME = "api:polar_auth"
AUTH_CALLBACK_PATH = "/api/polar_auth"

ENDPOINTS = {
    CONF_DAILY_ACTIVITY: PolarEndpoint(
        'daily_activity',
        'activity-log',
        'created',
        'list_activities',
        'get_activity_summary'),
    CONF_TRAINING_DATA: PolarEndpoint(
        'training_data',
        'exercises',
        'start-time',
        'list_exercises',
        'get_exercise_summary'),
    CONF_PHYSICAL_INFO: PolarEndpoint(
        'physical_info',
        'physical-informations',
        'created',
        'list_physical_infos',
        'get_physical_info')}

class PolarEndpointType:
    """Base class for modeling Polar endpoints."""

    def __init__(self, name, result_name, timestamp_name, list_method, get_method):
        self.name = name
        self.result_name = result_name
        self.timestamp_name = timestamp_name
        self.list_method = list_method
        self.get_method = get_method

RESOURCES = {
    CONF_DAILY_ACTIVITY: [
        PolarResource(
            'calories',
            'Calories',
            'kcal',
            'mdi:fire'),
        PolarResource(
            'active-calories',
            'Active Calories',
            'kcal',
            'mdi:fire'),
        PolarResource(
            'duration',
            'Duration',
            'mins',
            'mdi:clock'),
        PolarResource(
            'active-steps',
            'Active Steps',
            'steps',
            'mdi:walk')],
    CONF_TRAINING_DATA: [
        PolarResource(
            'device',
            'Device',
            None,
            None),
        PolarResource(
            'start-time',
            'Start Time',
            None,
            'mdi:clock'),
        PolarResource(
            'duration',
            'Duration',
            'mins',
            'mdi:clock'),
        PolarResource(
            'calories',
            'Calories',
            'kcal',
            'mdi:fire'),
        PolarResource(
            'distance',
            'Distance',
            'm',
            'mdi:map-marker'),
        PolarResource(
            'heart-rate/average',
            'Average Heart Rate',
            'bpm',
            'mdi:heart-pulse'),
        PolarResource(
            'heart-rate/maximum',
            'Maximum Heart Rate',
            'bpm',
            'mdi:heart-pulse'),
        PolarResource(
            'training-load',
            'Training Load',
            None,
            'mdi:run'),
        PolarResource(
            'sport',
            'Sport',
            None,
            None),
        PolarResource(
            'has-route',
            'Has Route',
            None,
            None),
        PolarResource(
            'club-id',
            'Club ID',
            None,
            None),
        PolarResource(
            'club-name',
            'Club Name',
            None,
            None),
        PolarResource(
            'detailed-sport-info',
            'Detailed Sport',
            None,
            None)],
    CONF_PHYSICAL_INFO: [
        PolarResource(
            'weight',
            'Weight',
            'kg',
            'mdi:weight-kilogram'),
        PolarResource(
            'height',
            'Height',
            'cm',
            'mdi:ruler'),
        PolarResource(
            'maximum-heart-rate',
            'Maximum Heart Rate',
            'bpm',
            'mdi:heart-pulse'),
        PolarResource(
            'resting-heart-rate',
            'Resting Heart Rate',
            'bpm',
            'mdi:heart-pulse'),
        PolarResource(
            'aerobic-threshold',
            'Aerobic Threshold',
            'bpm',
            None),
        PolarResource(
            'anaerobic-threshold',
            'Anaerobic Threshold',
            'bpm',
            None),
        PolarResource(
            'vo2-max',
            'VO2 Max',
            'L/min',
            None)]}

RESOURCE_NAMES = {
    endpoint: [ resource.name for resource in resources ]
        for endpoint, resources in RESOURCES.items() }

class PolarResource:
    """Base class for modeling Polar data."""

    def __init__(self, name, friendly_name, units, icon):
        """Constructor."""
        self.name = name
        self.friendly_name = friendly_name
        self.units = units
        self.icon = icon