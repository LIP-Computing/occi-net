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

import webob
import json
import copy

from ooi.api.helpers import BaseHelper
from occinet.wsgi import parsers

from ooi import utils


class OpenStackNet(BaseHelper):
    """Class to interact with the neutron API."""

    def __init__(self, app, neutron_version, neutron_endpoint):
        super(OpenStackNet, self).__init__(app, neutron_version)
        self.neutron_endpoint = neutron_endpoint

    translation = {"networks":{"occi.core.title":"name",
                   "occi.core.id":"network_id",
                   "occi.network.state":"status",
                   "project":"tenant_id",
                   "occi.core.title":"name"},
                   "subnet":{"occi.core.title":"name"}
                   }

    def _get_req(self, req, method,
                 path=None,
                 content_type="application/json",
                 body=None,
                 query_string=""):
        """Return a new Request object to interact with OpenStack.

        This method will create a new request starting with the same WSGI
        environment as the original request, prepared to interact with
        OpenStack. Namely, it will override the script name to match the
        OpenStack version. It will also override the path, content_type and
        body of the request, if any of those keyword arguments are passed.

        :param req: the original request
        :param path: new path for the request
        :param content_type: new content type for the request, defaults to
                             "application/json" if not specified
        :param body: new body for the request
        :param query_string: query string for the request, defaults to an empty
                             query if not specified
        :returns: a Request object
        """
        server = self.neutron_endpoint
        port = "9696"
        kwargs = {"http_version": "HTTP/1.1", "server_name": server, "server_port": port}
        try:
            if "HTTP_X-Auth-Token" in req.environ:
                token = req.environ["HTTP_X-Auth-Token"]
            else:
                token = req.environ["keystone.token_auth"].get_auth_ref(None)['auth_token']
            #project_id = req.environ["HTTP_X_PROJECT_ID"]
        except Exception:
            raise webob.exc.HTTPUnauthorized
        environ = {"HTTP_X-Auth-Token": token} #"HTTP_X_PROJECT_ID": project_id}

        new_req = webob.Request.blank(path=path, environ=environ,  base_url="/v2.0", **kwargs)
        new_req.script_name = self.openstack_version
        new_req.query_string = query_string
        new_req.method = method
        if path is not None:
            new_req.path_info = path
        if content_type is not None:
            new_req.content_type = content_type
        if body is not None:
            new_req.body = utils.utf8(body)


        return new_req

    def _make_get_request(self, req, path, parameters=None):
        """Create GET request
        This method create a GET Request instance
        :param req: the incoming request
        :param path: element location
        :param parameters: parameters to filter results
        """
        param = parsers.translate_parameters(self.translation["networks"],parameters)
        query_string = parsers.get_query_string(param)
        return self._get_req(req, path=path, query_string=query_string, method="GET")

    def _make_create_request(self, req, parameters):#TODO(jorgesece): Create test for it
        """Create CREATE request
        This method create a CREATE Request instance
        :param req: the incoming request
        :param parameters: parameters with values
        """
        path = "/networks"
        param = parsers.translate_parameters(self.translation["networks"], parameters)
        body = parsers.make_body(param)
        return self._get_req(req, path=path, content_type="application/json", body=json.dumps(body), method="POST")

    def _make_delete_request(self, req, path, parameters):
        """Create DELETE request
        This method create a DELETE Request instance
        :param req: the incoming request
        :param path: element location
        """
        param = parsers.translate_parameters(self.translation["networks"], parameters)
        id = param["network_id"]
        path = "%s/%s" % (path, id)
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
        return self.get_from_response(response, "networks", [])

    def get_network(self, req, id):
        """Get info from a network. It returns json code from the server
        :param req: the incoming network
        :param id: net identification
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
        """
        path = "/subnets/%s" % id
        req = self._make_get_request(req, path)
        response = req.get_response(self.app)

        return self.get_from_response(response, "subnet", {})

    def create_network(self, req, parameters):
        """Create a server.
        :param req: the incoming request
        :param parameters: parameters with values for the new network
        """
        req = self._make_create_request(req, parameters)
        response = req.get_response(self.app)
        return self.get_from_response(response, "network", {})

    def delete_network(self, req, parameters):
        """Delete network. It returns empty array
        :param req: the incoming network
        :param id: net identification
        """
        path = "/networks"
        req = self._make_delete_request(req, path, parameters)
        response = req.get_response(self.app)
        return response
