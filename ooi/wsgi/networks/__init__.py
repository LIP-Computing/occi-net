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

from ooi.wsgi import Resource


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

    def __call__(self, request, args): #todo(jorgesece): move process parameters to openstack driver
        """Control the method dispatch."""
        parameters = self._process_parameters(request)
        if parameters:
            args.update(parameters)

        return super(ResourceNet,self).__call__(request,args)
