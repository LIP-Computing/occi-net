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

from ooi.wsgi import Request as RequestOOI
from ooi.wsgi import Resource
from ooi.wsgi import Fault
from ooi.wsgi import ResourceExceptionHandler
from ooi.wsgi import ResponseObject
from ooi.wsgi import exception
from ooi.log import log as logging
from occinet.wsgi.parsers import ParserNet
from ooi import config

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


class Request(RequestOOI):

    def __init__(self, environ):
        super(Request,self).__init__(environ)
        self.parser = ParserNet(environ, None)

    def get_parser(self):
        return self.parser

    def get_parameter_list(self):
        return self.parser.get_attributes_from_headers()


class ResourceNet(Resource):
    def __init__(self, controller):
        super(ResourceNet, self).__init__(controller)

    @staticmethod
    def _process_parameters(req):
        param = req.get_parameter_list()
        content = None
        if param:
            content = {"parameters": param}
            del req.environ['HTTP_X_OCCI_ATTRIBUTE']
        return content

    def __call__(self, request, args):
        """Control the method dispatch."""
        parameters = self._process_parameters(request)
        if parameters:
            args.update(parameters)

        return super(ResourceNet,self).__call__(request,args)
