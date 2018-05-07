# -*- coding: utf-8 -*-
from __future__ import absolute_import

import base64
import logging
import sys

from boto3.session import Session

_logger = logging.getLogger(__name__)
_logger.addHandler(logging.StreamHandler(sys.stdout))
_logger.setLevel(logging.INFO)


class EcrClient(object):

    def __init__(self, profile_name=None, region_name=None,
                 debug=False):
        if debug:
            _logger.setLevel(logging.DEBUG)
        self._session = Session(profile_name=profile_name,
                                region_name=region_name)
        self._client = self._session.client('ecr')

    def get_authorization_token(self, registry_id=None):
        if registry_id:
            response = self._client.get_authorization_token(registryIds=[registry_id])
        else:
            response = self._client.get_authorization_token()
        auth_token = response['authorizationData'][0]['authorizationToken']
        registry = response['authorizationData'][0]['proxyEndpoint']
        username, password = tuple(base64.b64decode(auth_token).decode('utf-8').split(':'))
        return username, password, registry
