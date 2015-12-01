# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
#


import copy
import json
import os

import six.moves.urllib.parse as urlparse
import webob.exc

from occinet.drivers import base


class OpenStackNet(base.BaseHelper):
    """Class to interact with the neutron API."""

    @staticmethod
    def tenant_from_req(req):
        """Return the tenant id
        This method retrieve a list of network to which the tenant has access.
        :param req: the original request
        :returns: tenant Id
        """
        try:
            return req.environ["keystone.token_auth"].user.project_id
        except AttributeError:
            return req.environ["keystone.token_info"]["token"]["project"]["id"]

    def _get_index_req(self, req):
        """Return a new Request object to interact with OpenStack.
        This method retrieve a request ready to list networks
        :param req: the original request

        :returns: request modified
        """
        tenant_id = self.tenant_from_req(req)
        path = "/networks?%s" % tenant_id
        return self._get_req(req, path=path, method="GET")

    def index(self, req):
        """Get a list of servers for a tenant.
        This method retrieve a list of network to which the tenant has access.
        :param req: the incoming request
        """
        os_req = self._get_index_req(req)
        response = os_req.get_response(self.app)
        return self.get_from_response(response, "networks", [])