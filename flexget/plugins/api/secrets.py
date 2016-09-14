from __future__ import unicode_literals, division, absolute_import
from builtins import *  # pylint: disable=unused-import, redefined-builtin

import logging

from flask import request

from flexget.api.app import api
from flexget.api.responses import empty_response
from flexget.api.models import APIResource
from flexget.plugins.modify.config_secrets import secrets_from_db, secrets_to_db

log = logging.getLogger('secrets')

secrets_api = api.namespace('secrets', description='View and edit secrets')


@secrets_api.route('/')
class SecretsAPI(APIResource):

    @api.response(200, model=empty_response)
    def get(self, session=None):
        return secrets_from_db()

    @api.response(201, 'Successfully updated secrets file')
    @api.validate(empty_response)
    @api.doc(description='Note that editing secrets may not be persistent, depending on user config')
    def put(self, session=None):
        data = request.json
        secrets_to_db(data)
        # This will trigger reloading the secrets file
        self.manager.validate_config()
        return secrets_from_db(), 201
