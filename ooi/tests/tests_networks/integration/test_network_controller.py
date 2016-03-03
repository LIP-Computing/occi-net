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


from ooi.tests.tests_networks.integration import  TestIntegration

from ooi import exception
from ooi.wsgi import Request
from ooi.api.networks import network
from ooi.occi.infrastructure import network_extend
from ooi.tests.tests_networks.integration.keystone.session import KeySession
from ooi.tests.tests_networks import fakes



class TestIntegrationNetwork(TestIntegration):

    def setUp(self):
        super(TestIntegrationNetwork, self).setUp()
        self.req = Request(KeySession().create_request(self.session, path="/", environ={}, headers=None).environ)

        self.controller = network.Controller("http://127.0.0.1:9696/v2.0")

    def test_list(self):
        list = self.controller.index(self.req)
        self.assertIsInstance(list.resources[0], network_extend.Network)
        sortedList = sorted(list.resources, key=lambda Network: Network.title, reverse=True)
        self.assertEqual("public", sortedList[0].title)

    def test_list_by_tenant(self):
        self.req.headers = fakes.create_header(None,None, self.project_id)
        list = self.controller.index(self.req)
        sortedList = sorted(list.resources, key=lambda Network: Network.title, reverse=True)
        self.assertIsInstance(sortedList[0], network_extend.Network)
      #  self.assertEqual("public", sortedList[0].title)

    def test_list_by_tenant_error(self):
        self.req.headers = fakes.create_header(None,None, "noexits")
        list = self.controller.index(self.req)
        self.assertIs(0, list.resources.__len__())

    def test_show_network(self):
        net = self.controller.show(self.req, self.public_network)
        self.assertEqual("public", net.title)

    def test_run_up_network(self):
        body = None
        out = None
        try:
            net = self.controller.run_action(self.req,self.public_network,body)
        except Exception as e:
            out = e
        self.assertIsInstance(out, exception.NotFound)

    def test_create_network_no_subnetwork(self):
        #Create
        parameters = { "occi.core.title":self.new_network_name,
                     }
        self.req.headers = fakes.create_header(parameters,None)
        try:
            self.controller.create(self.req)
        except Exception as e:
            out = e
        self.assertIsInstance(out, exception.Invalid)

    def test_create_delete_network_with_subnet(self):
        list1 = self.controller.index(self.req)
        ip_version = 4
        cidr = "11.0.0.1/24"
        gateway = "11.0.0.3"
        #Create
        parameters ={"occi.core.title": self.new_network_name,
                    "occi.network.ip_version": ip_version,
                    "occi.networkinterface.address": cidr,
                    "occi.networkinterface.gateway": gateway,
                     }
        self.req.headers = fakes.create_header(parameters,None,self.project_id)
        net = self.controller.create(self.req)
        self.assertEqual(self.new_network_name, net.title)
        self.req.headers.pop("X-OCCI-Attribute")
        self.req.headers.pop("X-PROJECT-ID")
        list2 = self.controller.index(self.req)
        self.assertEqual(list1.resources.__len__() + 1, list2.resources.__len__())

         # Delete
        #response = self.controller.delete(self.req, {"attributes":{"occi.core.id": net.id}})
        response = self.controller.delete(self.req, net.id)
        self.assertIsInstance(response, list)
        list3 = self.controller.index(self.req)
        self.assertEqual(list1.resources.__len__(), list3.resources.__len__())


"""
    def test_delete_network(self):
        response = self.controller.delete(self.req, self.new_network_id)

        self.assertEqual(204, response.status_code)
"""