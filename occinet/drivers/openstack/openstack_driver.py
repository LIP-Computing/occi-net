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

import six.moves.urllib.parse as urlparse

from ooi import exception
from occinet.drivers import base
from occinet.wsgi import parsers

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
            return req.environ["HTTP_X_PROJECT_ID"]
        except KeyError:
            raise exception.Forbidden(reason="Cannot find project ID")

    def _get_index_req(self, req, _query_string=None):
        """Return a new Request object to interact with OpenStack.
        This method retrieve a request ready to list networks
        :param req: the original request
        :param _query_string: additional query information

        :returns: request modified
        """

        _path = "/networks"
        return self._get_req(req, path=_path, method="GET", query_string=_query_string)

    def index(self, req, parameters=None):
        """Get a list of networks.
        This method retrieve a list of network to which the tenant has access.
        :param req: the incoming request
        :param parameters: parameters to filter results
        """
        query_string = None
        if parameters is not None:
            query_string = parsers.get_query_string(parameters)
        os_req = self._get_index_req(req, query_string)
        response = os_req.get_response(self.app)

        return self.get_from_response(response, "networks", [])

    def get_network(self, req, parameters):
        """Get info from a network. It returns json code from the server

        :param req: the incoming network
        :param parameters: parameters to filter results (networkID,owner tenant)
        """

        req = self._get_network_req(req, parameters)
        response = req.get_response(self.app)

        return self.get_from_response(response, "network", {})

    def _get_network_req(self, req, parameters):
        path = "/networks"
        query_string = parsers.get_query_string(parameters)

        return self._get_req(req, path=path, query_string=query_string, method="GET")

    # RETRIEVE SUBNET DETAILS
    def get_flavor(self, req, parameters):
        """Get information from a flavor.

        :param req: the incoming request
        :param parameters: parameters to filter results (subnetID,networkID,owner tenant)
        """
        req = self._get_flavor_req(req, parameters)
        response = req.get_response(self.app)

        return self.get_from_response(response, "flavor", {})

    def _get_subnets_req(self, req, parameters):
        path = "/subnets"
        query_string = parsers.get_query_string(parameters)

        return self._get_req(req, path=path, query_string=query_string, method="GET")