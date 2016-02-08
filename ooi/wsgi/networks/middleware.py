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

from ooi.wsgi import Resource, OCCIMiddleware
from ooi.log import log as logging
#from ooi.wsgi import OCCIMiddleware
#from ooi.wsgi import Resource
from ooi.api.networks.network import Controller

LOG = logging.getLogger(__name__)


class ResourceNet(Resource):
    def __init__(self, controller):
        super(ResourceNet, self).__init__(controller)

    @staticmethod
    def _process_parameters(req):
        content = None
        param = None
        parser = req.get_parser()(req.headers, req.body)
        if 'Category' in req.headers:
            param = parser.parse()
        else:
            attrs = parser.parse_attributes(req.headers)
            if attrs.__len__():
                param = {"attributes": attrs}
        if param:
            content = {"parameters": param}
        return content

    def __call__(self, request, args):
        """Control the method dispatch."""
        parameters = self._process_parameters(request)
        if parameters:
            args.update(parameters)

        return super(ResourceNet,self).__call__(request,args)

class OCCINetworkMiddleware(OCCIMiddleware):

    def __init__(self, application, neutron_version="/v2.0", neutron_endpoint="0.0.0.0"):
        super(OCCINetworkMiddleware, self).__init__(application, openstack_version="/v2.1")
        self.neutron_version = neutron_version
        self.neutron_endpoint = neutron_endpoint
        self._setup_net_routes()

    def _create_net_resource(self, controller): #fixme(jorgesece): wsgi unitttest do not work, it is not using FakeApp
        return ResourceNet(controller(self.application, self.neutron_version, self.neutron_endpoint))

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
        self.resources["networks"] = self._create_net_resource(Controller)
        self._setup_net_resources_routes("networks", self.resources["networks"])

    # def process_response(self, response):
    #     """Process a response by adding our headers."""
    #     network_string = "ooi/%s %s" % (version.version_string,
    #                                     self.occi_string)
    #
    #     headers = (("network", network_string),) #fixme(jorgesece): it should come from a paremeter (server/network)
    #     if isinstance(response, Fault):
    #         for key, val in headers:
    #             response.wrapped_exc.headers.add(key, val)
    #     else:
    #         for key, val in headers:
    #             response.headers.add(key, val)
    #     return response
    #
    #
    # @webob.dec.wsgify(RequestClass=Request) #fixme(jorgesece): Move parameters and parser from Request to driver
    # def __call__(self, req):
    #     response = self.process_request(req)
    #     if not response:
    #         response = req.get_response(self.application)
    #
    #     return self.process_response(response)



