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
import webob.dec

from ooi.wsgi import OCCIMiddleware as OCCIMiddleware
from ooi.wsgi import Fault

from occinet.wsgi import parsers

from ooi.wsgi import ResourceExceptionHandler
from ooi.wsgi import ResponseObject
from ooi.wsgi import serializers
from ooi import exception

from ooi import version
from ooi.api import query

import occinet.api.network


class OCCINetworkMiddleware(OCCIMiddleware):

    def __init__(self, application, openstack_version="/v2.1"):
        super(OCCINetworkMiddleware, self).__init__(application, openstack_version)

    def _setup_resource_routes(self, resource, controller):
        path = "/" + resource
         # These two could be removed for total OCCI compliance
        self.mapper.connect(resource, path, controller=controller,
                            action="index",  conditions=dict(method=["GET"]))
        self.mapper.connect(resource, path + "/{id}", controller=controller,
                            action="show", conditions=dict(method=["GET"]))

    def _setup_routes(self):
        self.mapper.redirect("", "/")

        self.resources["query"] = self._create_resource(query.Controller)
        self.mapper.connect("query", "/-/",
                            controller=self.resources["query"],
                            action="index")

        # RFC5785, OCCI section 3.6.7
        self.mapper.connect("query", "/.well-known/org/ogf/occi/-/",
                            controller=self.resources["query"],
                            action="index")
        self.resources["networks"] = self._create_resource(occinet.api.network.Controller)
        self._setup_resource_routes("networks", self.resources["networks"])

    def process_response(self, response):
        """Process a response by adding our headers."""
        network_string = "ooi/%s %s" % (version.version_string,
                                        self.occi_string)

        headers = (("network", network_string),)
        if isinstance(response, Fault):
            for key, val in headers:
                response.wrapped_exc.headers.add(key, val)
        else:
            for key, val in headers:
                response.headers.add(key, val)
        return response

    def process_request(self, req):
        if req.user_agent:

            match = re.search(r"\bOCCI/\d\.\d\b", req.user_agent)
            if match and self.occi_string != match.group():
                return Fault(webob.exc.HTTPNotImplemented(
                             explanation="%s not supported" % match.group()))

        match = self.mapper.match(req.path_info, req.environ)
        if not match:
            return Fault(webob.exc.HTTPNotFound())
        #TODO(jorgesece): create parse method to create the array from HTTP_OCCI_ATTRIBUTE
        if( 'HTTP_X_OCCI_ATTRIBUTE' in req.environ ):
            match["parameters"] = parsers.get_attributes_from_headers(req.environ)
            #match["parameters"] = {"tenant_id" : req.environ['HTTP_X_PROJECT_ID']} # req.environ['HTTP_X_OCCI_ATTRIBUTE']
            del req.environ['HTTP_X_OCCI_ATTRIBUTE']
        method = match["controller"]
        return method(req, match)


