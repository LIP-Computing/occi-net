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


from keystone.session import KeySession
from occinet.api import network
#from ooi.occi.infrastructure import network as network_occi

from occinet.infrastructure import network_extend
from ooi.tests import base


class TestIntegrationNetwork(base.TestController):

    def setUp(self):
        super(TestIntegrationNetwork, self).setUp()
        self.controller = network.Controller(None, "/v2.0")
        self.project_id = "86bf9730b23d4817b431f4c34cc9cc8e"
        self.public_network = "cd58eade-79a1-4633-8fb7-c7d8a030c942"
        self.new_network_name = "networkOCCINET"
        self.req = KeySession().create_request_conection("admin", "stack1", self.project_id)

    def test_list(self):
        list = self.controller.index(self.req, None)
        self.assertIsInstance(list.resources[0], network_extend.Network)
        sortedList = sorted(list.resources, key=lambda Network: Network.title, reverse=True)
        self.assertEqual("public", sortedList[0].title)

    def test_list_by_tenant(self):
        tenant_id = self.req.environ["HTTP_X_PROJECT_ID"]
        list = self.controller.index(self.req, {"tenant_id": self.project_id})
        sortedList = sorted(list.resources, key=lambda Network: Network.title, reverse=True)
        self.assertIsInstance(sortedList[0], network_extend.Network)
        self.assertEqual("public", sortedList[0].title)

    def test_list_by_tenant_error(self):
        list = self.controller.index(self.req, {"tenant_id": "noexits"})
        self.assertIs(0, list.resources.__len__())

    def test_show_network(self):
        net = self.controller.show(self.req, self.public_network)
        self.assertEqual("public", net.title)

    def test_show_network_with_subnet(self):
        net = self.controller.show(self.req, self.public_network)
        self.assertEqual("public", net.title)
        self.assertEqual(1, net.subnets.__len__() )
        self.assertEqual("public-subnet", net.subnets[0].title )

    def test_create_delete_network(self):
        list1 = self.controller.index(self.req, None)
        #Create
        net = self.controller.create(self.req, {"name": self.new_network_name,"tenant_id": self.project_id})
        self.assertEqual(self.new_network_name, net.title)
        list2 = self.controller.index(self.req, None)
        self.assertEqual(list1.resources.__len__() + 1, list2.resources.__len__())

        # Delete
        response = self.controller.delete(self.req, net.id)
        self.assertEqual(204, response.status_code)
        list3 = self.controller.index(self.req, None)
        self.assertEqual(list1.resources.__len__(), list3.resources.__len__())

"""
    def test_delete_network(self):
        response = self.controller.delete(self.req, self.new_network_id)

        self.assertEqual(204, response.status_code)
"""