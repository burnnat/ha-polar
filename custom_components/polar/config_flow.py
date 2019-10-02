"""Config flow for Polar Flow."""
import logging

from collections import OrderedDict

import aiohttp
import requests
import voluptuous as vol

from homeassistant import config_entries, data_entry_flow
from homeassistant.core import callback
from homeassistant.helpers import config_entry_flow
from homeassistant.components.http import HomeAssistantView

from accesslink import AccessLink

from .const import DOMAIN, AUTH_CALLBACK_NAME, AUTH_CALLBACK_PATH

_LOGGER = logging.getLogger(__name__)

has_oauth_callback = False

def setup_oauth_callback(hass):
    callback_url = f"{hass.config.api.base_url}{AUTH_CALLBACK_PATH}"

    if not has_oauth_callback:
        hass.http.register_view(PolarAuthCallbackView())
    
    return callback_url

@config_entries.HANDLERS.register(DOMAIN)
class PolarConfigFlow(config_entries.ConfigFlow):
    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_CLOUD_POLL

    def __init__(self):
        self.data = None
        self.accesslink_client = None

    @property
    def accesslink(self):
        callback_url = setup_oauth_callback(self.hass)

        if not self.accesslink_client:
            self.accesslink_client = AccessLink(
                client_id=self.data['client_id'],
                client_secret=self.data['client_secret'],
                redirect_url=callback_url)

        return self.accesslink_client

    async def async_step_user(self, user_input=None):
        _LOGGER.debug('Starting user config flow')
        return await self.async_step_client(user_input)

    async def async_step_import(self, user_input=None):
        _LOGGER.debug('Starting import config flow')
        return await self.async_step_client(user_input)

    async def async_step_client(self, user_input=None):
        if user_input is not None:
            self.data = {
                'client_id': user_input['client_id'],
                'client_secret': user_input['client_secret']}
            
            return await self.async_step_oauth()

        data_schema = OrderedDict()
        data_schema[vol.Required('client_id')] = str
        data_schema[vol.Required('client_secret')] = str

        callback_url = setup_oauth_callback(self.hass)

        return self.async_show_form(
            step_id='client',
            description_placeholders={
                'callback_url': callback_url
            },
            data_schema=vol.Schema(data_schema)
        )

    async def async_step_oauth(self, user_input=None):
        if not user_input:
            return self.async_external_step(
                step_id='oauth',
                url=self.accesslink.get_authorization_url(state=self.flow_id)
            )

        token_response = self.accesslink.get_access_token(user_input['code'])

        self.data['user_id'] = token_response['x_user_id']
        self.data['access_token'] = token_response['access_token']

        return self.async_external_step_done(next_step_id='finish')

    async def async_step_finish(self, user_input=None):
        data = user_input or self.data or {}

        try:
            self.accesslink.users.register(access_token=data['access_token'])
        except requests.exceptions.HTTPError as err:
            # Error 409 Conflict means that the user has already been registered for this client, which is okay.
            if err.response.status_code != 409:
                raise err

        return self.async_create_entry(
            title='Polar',
            data=data
        )

class PolarAuthCallbackView(HomeAssistantView):
    """Polar Accesslink Authorization Callback View."""

    requires_auth = False
    url = AUTH_CALLBACK_PATH
    name = AUTH_CALLBACK_NAME

    @callback
    async def get(self, request):
        """Receive authorization token."""
        hass = request.app['hass']

        flow_id = request.query['state']
        code = request.query['code']

        _LOGGER.debug('Received auth code from external call')

        try:
            await hass.config_entries.flow.async_configure(flow_id, {'code': code})

            return aiohttp.web_response.Response(
                status=200,
                headers={'content-type': 'text/html'},
                text='<script>window.close()</script>',
            )

        except data_entry_flow.UnknownFlow:
            return aiohttp.web_response.Response(status=400, text='Unknown flow')
