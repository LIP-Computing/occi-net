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
from ooi.wsgi.parsers import HeaderParser as ParserNet
from ooi import config

LOG = logging.getLogger(__name__)


occi_opts = [
    config.cfg.StrOpt('neutron_endpoint',
                      default="127.0.0.1",
                      help='Neutron end point which access to the Neutron Resfult API '
                      'will listen.'),
    config.cfg.StrOpt('neutron_version',
                      default="/v2.0",
                      help='Neutron Resfult API version '
                      'will listen.'),
    config.cfg.IntOpt('occinet_listen_port',
                      default=8787,
                      help='The port on which the OCCI (ooi) API '
                      'will listen.'),
    config.cfg.IntOpt('occinet_workers',
                      help='Number of workers for OCCI (ooi) API service. '
                      'The default will be equal to the number of CPUs '
                      'available.'),
    config.cfg.IntOpt('occinet_workers',
                      help='Number of workers for OCCI (ooi) API service. '
                      'The default will be equal to the number of CPUs '
                      'available.'),
]

CONF = config.cfg.CONF
CONF.register_opts(occi_opts)


# class Request(RequestOOI):
#
#     def __init__(self, environ):
#         super(Request,self).__init__(environ)
#         self.parser = HeaderParser(self.headers, None)
#
#     def get_parser(self):
#         return self.parser


# class ResourceNet(Resource):
#     def __init__(self, controller):
#         super(ResourceNet, self).__init__(controller)
#
#     @staticmethod
#     def _process_parameters(req):
#         content = None
#         param = None
#         parser = req.get_parser()(req.headers, req.body)
#         if 'Category' in req.headers:
#             param = parser.parse()
#         else:
#             attrs = parser.parse_attributes(req.headers)
#             if attrs.__len__():
#                 param = {"attributes": attrs}
#         if param:
#             content = {"parameters": param}
#         return content
#
#     def __call__(self, request, args):
#         """Control the method dispatch."""
#         parameters = self._process_parameters(request)
#         if parameters:
#             args.update(parameters)
#
#         return super(ResourceNet,self).__call__(request,args)
