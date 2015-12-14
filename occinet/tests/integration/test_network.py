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


from keystone.session import KeySession
from occinet.api import network
#from ooi.occi.infrastructure import network as network_occi

from occinet.infrastructure import network_extend
from ooi.tests import base


class TestIntegrationNetwork(base.TestController):

    def setUp(self):
        super(TestIntegrationNetwork, self).setUp()
        self.controller = network.Controller(None, "/v2.0")
        self.req = KeySession().create_request_conection("dev", "passwd", "6271876e5bea4935a98cf10840f8dcb6")
        self.public_network="3e75d5af-f5b9-4a69-bef6-7539f3323a73"

    def test_list(self):
        list = self.controller.index(self.req, None)

        self.assertIsInstance(list.resources[0], network_extend.Network)
        self.assertEqual("public", list.resources[0].title)

    def test_list_by_tenant(self):
        tenant_id = self.req.environ["HTTP_X_PROJECT_ID"]
        list = self.controller.index(self.req, {"tenant_id": "c7edc47ad16041d9985de95f4443a3ab"})

        self.assertIsInstance(list.resources[0], network_extend.Network)
        self.assertEqual("public", list.resources[0].title)

    def test_list_by_tenant_error(self):

        list = self.controller.index(self.req, {"tenant_id": "noexits"})

        self.assertIs(0, list.resources.__len__())

    def test_show_network(self):

        net = self.controller.show(self.req, self.public_network)
        self.assertEqual("public", net.title)
