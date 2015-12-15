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

    def _create_os_request(self, req, path, parameters=None):

        query_string = parsers.get_query_string(parameters)

        return self._get_req(req, path=path, query_string=query_string, method="GET")


    def index(self, req, parameters=None):
        """Get a list of networks.
        This method retrieve a list of network to which the tenant has access.
        :param req: the incoming request
        :param parameters: parameters to filter results
        """
        path = "/networks"
        os_req = self._create_os_request(req, path, parameters)

        response = os_req.get_response(self.app)

        return self.get_from_response(response, "networks", [])

    def get_network(self, req, id, parameters=None):
        """Get info from a network. It returns json code from the server

        :param req: the incoming network
        :param id: net identification
        :param parameters: parameters to filter results (networkID,owner tenant)
        """
        path = "/networks/%s" % id
        req = self._create_os_request(req, path, parameters)

        response = req.get_response(self.app)

        resp = self.get_from_response(response, "network", {})
        resp["status"] = parsers.network_status(resp["status"]);

        return resp


    # RETRIEVE SUBNET DETAILS
    def get_subnets(self, req, id, parameters=None):
        """Get information from a flavor.

        :param req: the incoming request
        :param id: subnet identification
        :param parameters: parameters to filter results (subnetID,networkID,owner tenant)
        """
        path = "/subnets/%s" % id
        req = self._create_os_request(req, path, parameters)

        response = req.get_response(self.app)

        return self.get_from_response(response, "subnet", {})

