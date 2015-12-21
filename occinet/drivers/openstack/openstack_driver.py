# -*- coding: utf-8 -*-

# Copyright 2015 LIP - Lisbon
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
import json

from ooi import exception
from occinet.drivers import base
from occinet.wsgi import parsers


class OpenStackNet(base.BaseHelper):
    """Class to interact with the neutron API."""

    def _make_get_request(self, req, path, parameters=None):

        query_string = parsers.get_query_string(parameters)

        return self._get_req(req, path=path, query_string=query_string, method="GET")

    def _make_create_request(self, req, parameters):

        path = "/networks"
        body = parsers.make_body(parameters)

        return self._get_req(req, path=path, content_type="application/json", body=json.dumps(body), method="POST")

    def _make_delete_request(self, req, path):

        return self._get_req(req, path=path, method="DELETE")

    def index(self, req, parameters=None):
        """Get a list of networks.
        This method retrieve a list of network to which the tenant has access.
        :param req: the incoming request
        :param parameters: parameters to filter results
        """
        path = "/networks"
        os_req = self._make_get_request(req, path, parameters)

        response = os_req.get_response(self.app)

        response.body = os_req.application_url

        return self.get_from_response(response, "networks", [])

    def get_network(self, req, id):
        """Get info from a network. It returns json code from the server

        :param req: the incoming network
        :param id: net identification
        :param parameters: parameters to filter results (networkID,owner tenant)
        """
        path = "/networks/%s" % id
        req = self._make_get_request(req, path)

        response = req.get_response(self.app)

        resp = self.get_from_response(response, "network", {})
        resp["status"] = parsers.network_status(resp["status"]);

        return resp

    def get_subnet(self, req, id):
        """Get information from a subnet.

        :param req: the incoming request
        :param id: subnet identification
        :param parameters: parameters to filter results (subnetID,networkID,owner tenant)
        """
        path = "/subnets/%s" % id
        req = self._make_get_request(req, path)
        response = req.get_response(self.app)

        return self.get_from_response(response, "subnet", {})

    def create_network(self, req, parameters):
        """Create a server.

        :param req: the incoming request
        :param parameters: parameters for the new network
        """
        req = self._make_create_request(req, parameters)

        response = req.get_response(self.app)
        # We only get one server
        return self.get_from_response(response, "network", {})

    def delete_network(self, req, id):
        """Delete network. It returns id

        :param req: the incoming network
        :param id: net identification

        """
        path = "/networks/%s" % id
        req = self._make_delete_request(req, path)
        response = req.get_response(self.app)

        return response