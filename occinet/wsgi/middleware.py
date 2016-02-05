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

import re
import routes
import webob.dec


from ooi.wsgi import Fault
from ooi.log import log as logging
from ooi import version
from ooi.wsgi import OCCIMiddleware
import occinet.api.network
from occinet.api import query
from occinet.wsgi import ResourceNet
from occinet.wsgi import Request

LOG = logging.getLogger(__name__)


class OCCINetworkMiddleware(OCCIMiddleware):

    def __init__(self, application, neutron_version="/v2.0", neutron_endpoint="0.0.0.0"):
        super(OCCINetworkMiddleware, self).__init__(application, openstack_version="/v2.1")
        self.neutron_version = neutron_version
        self.neutron_endpoint = neutron_endpoint
        self._setup_net_routes()

    def _create_net_resource(self, controller): #fixme(jorgesece): wsgi unitttest do not work, it is not using FakeApp
        return ResourceNet(controller(None, self.neutron_version, self.neutron_endpoint))

    def _setup_net_resources_routes(self, resource, controller):
        path = "/" + resource
         # These two could be removed for total OCCI compliance
        self.mapper.connect(resource, path, controller=controller,
                            action="index",  conditions=dict(method=["GET"]))
        self.mapper.connect(resource, path, controller=controller,
                            action="create", conditions=dict(method=["POST"]))
        #OK
        self.mapper.connect(resource, path + "/", controller=controller,
                            action="index",  conditions=dict(method=["GET"]))
        self.mapper.connect(resource, path + "/", controller=controller,
                            action="create", conditions=dict(method=["POST"]))
        self.mapper.connect(resource, path + "/{id}", controller=controller,
                            action="show", conditions=dict(method=["GET"]))
        self.mapper.connect(resource, path, controller=controller,
                            action="delete", conditions=dict(method=["DELETE"]))

    def _setup_net_routes(self):
        self.mapper.redirect("", "/")
        # self.resources["query"] = self._create_net_resource(query.Controller)
        # self.mapper.connect("query", "/-/", controller=self.resources["query"],
        #                     action="index")
        # # RFC5785, OCCI section 3.6.7
        # self.mapper.connect("query", "/.well-known/org/ogf/occi/-/", controller=self.resources["query"],
        #                     action="index")

        self.resources["networks"] = self._create_net_resource(occinet.api.network.Controller)
        self._setup_net_resources_routes("networks", self.resources["networks"])

    def process_response(self, response):
        """Process a response by adding our headers."""
        network_string = "ooi/%s %s" % (version.version_string,
                                        self.occi_string)

        headers = (("network", network_string),) #fixme(jorgesece): it should come from a paremeter (server/network)
        if isinstance(response, Fault):
            for key, val in headers:
                response.wrapped_exc.headers.add(key, val)
        else:
            for key, val in headers:
                response.headers.add(key, val)
        return response


    @webob.dec.wsgify(RequestClass=Request) #fixme(jorgesece): Move parameters and parser from Request to driver
    def __call__(self, req):
        response = self.process_request(req)
        if not response:
            response = req.get_response(self.application)

        return self.process_response(response)



