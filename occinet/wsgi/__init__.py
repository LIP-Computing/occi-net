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

from occinet.wsgi.parsers import ParserNet


class Request(RequestOOI):

    def __init__(self, environ):
        super(Request,self).__init__(environ)
        self.parser = ParserNet(environ, None)

    def get_parser(self):
        return self.parser


class ResourceNet(Resource):
    def __init__(self, controller):
        super(ResourceNet, self).__init__(controller)
    @staticmethod
    def _process_parameters(req):
        if( 'HTTP_X_OCCI_ATTRIBUTE' in req.environ ):
            parameters = ParserNet(req.environ,None).get_attributes_from_headers()
            #match["parameters"] = {"tenant_id" : req.environ['HTTP_X_PROJECT_ID']} # req.environ['HTTP_X_OCCI_ATTRIBUTE']
            del req.environ['HTTP_X_OCCI_ATTRIBUTE']

    def __call__(self, request, args):
        """Control the method dispatch."""
        action_args = self.get_action_args(args)
        action = action_args.pop('action', None)
        try:
            accept = request.get_best_match_content_type()
            content_type = request.get_content_type()
        except exception.InvalidContentType as e:
            msg = e.format_message()
            return Fault(webob.exc.HTTPNotAcceptable(explanation=msg))

        body = request.body

        # Get the implementing method
        try:
            method = self.get_method(request, action,
                                     content_type, body)
        except (AttributeError, TypeError):
            return Fault(webob.exc.HTTPNotFound())
        except KeyError as ex:
            msg = "There is no such action: %s" % ex.args[0]
            return Fault(webob.exc.HTTPBadRequest(explanation=msg))

        contents = {}
        if request.should_have_body():
            # allow empty body with PUT and POST
            if request.content_length == 0:
                contents = {'body': None}
            else:
                contents["body"] = body

        parameters = request.get_parser().get_attributes_from_headers()
        if parameters:
            contents["parameters"] = parameters

        action_args.update(contents)

        response = None
        try:
            with ResourceExceptionHandler():
                action_result = self.dispatch(method, request, action_args)
        except Fault as ex:
            response = ex

        # No exceptions, so create a response
        # NOTE(aloga): if the middleware returns None, the pipeline will
        # continue, but we do not want to do so, so we convert the action
        # result to a ResponseObject.
        if not response:
            if isinstance(action_result, ResponseObject):
                resp_obj = action_result
            else:
                resp_obj = ResponseObject(action_result)

            response = resp_obj.serialize(request, accept,
                                          self.default_serializers)
        return response