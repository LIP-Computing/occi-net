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

import occinet.api.network
from ooi.wsgi import OCCIMiddleware as BaseMiddleware


class OCCIMiddleware(BaseMiddleware):

    def __init__(self, application, openstack_version=None):
         super(OCCIMiddleware, self).__init__(application, openstack_version)
         self.resources["networks"] = self._create_resource(occinet.api.network.Controller)
         self._setup_resource_routes("networks", self.resources["networks"])