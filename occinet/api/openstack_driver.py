# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
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


import copy
import json
import os

import six.moves.urllib.parse as urlparse
import webob.exc

from occinet.drivers import request


class OpenStackNet(request.BaseHelper):
    """Class to interact with the nova API."""

    @staticmethod
    def tenant_from_req(req):
        try:
            return req.environ["keystone.token_auth"].user.project_id
        except AttributeError:
            return req.environ["keystone.token_info"]["token"]["project"]["id"]

    def _get_index_req(self, req):
        tenant_id = self.tenant_from_req(req)
        path = "/%s/servers" % tenant_id
        return self._get_req(req, path=path, method="GET")
