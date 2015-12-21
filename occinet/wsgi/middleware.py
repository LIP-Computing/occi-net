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
import routes
import routes.middleware

from ooi.wsgi import OCCIMiddleware as OCCIMiddleware
from ooi.wsgi import Fault
from ooi.log import log as logging

from ooi import config
from ooi import version
from ooi.api import query

import occinet.api.network
from occinet.wsgi import ResourceNet
from occinet.wsgi import Request

LOG = logging.getLogger(__name__)

occi_opts = [
    config.cfg.StrOpt('ooi_listen',
                      default="0.0.0.0",
                      help='The IP address on which the OCCI (ooi) API '
                      'will listen.'),
    config.cfg.IntOpt('ooi_listen_port',
                      default=8787,
                      help='The port on which the OCCI (ooi) API '
                      'will listen.'),
    config.cfg.IntOpt('ooi_workers',
                      help='Number of workers for OCCI (ooi) API service. '
                      'The default will be equal to the number of CPUs '
                      'available.'),
]

CONF = config.cfg.CONF
CONF.register_opts(occi_opts)


class OCCINetworkMiddleware(object):

    occi_version = "1.1"
    occi_string = "OCCI/%s" % occi_version

    @classmethod
    def factory(cls, global_conf, **local_conf):
        """Factory method for paste.deploy."""
        LOG.debug("Factory definition")
        def _factory(app):

            conf = global_conf.copy()
            conf.update(local_conf)
            return cls(app, **local_conf)
        return _factory

    def __init__(self, application, openstack_version="/v2.1"):
        self.application = application
        self.openstack_version = openstack_version

        self.resources = {}

        self.mapper = routes.Mapper()
        self._setup_routes()

    def _create_resource(self, controller):
        return ResourceNet(controller(self.application, self.openstack_version))

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
        method = match["controller"]
        return method(req, match)

    @webob.dec.wsgify(RequestClass=Request)
    def __call__(self, req):
        response = self.process_request(req)
        if not response:
            response = req.get_response(self.application)

        return self.process_response(response)



