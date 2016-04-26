# -*- coding: utf-8 -*-

# Copyright 2016 LIP - Lisbon
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
from ooi.api import network as net_controler
from ooi.occi.infrastructure import network
from ooi.tests.tests_networks.integration.keystone.session import KeySession
from ooi.tests import fakes_neutron as fakes


class TestIntegrationNetworkNeutron(TestIntegration):

    def setUp(self):
        super(TestIntegrationNetworkNeutron, self).setUp()
        self.req = Request(
            KeySession().create_request(self.session, path="/",
                                        environ={},
                                        headers={
                                            "X_PROJECT_ID": self.project_id
                                        }).environ)

        self.controller = net_controler.Controller(neutron_endpoint="http://127.0.0.1:9696/v2.0")

    def test_list(self):
        list = self.controller.index(self.req)
        self.assertIsInstance(list.resources[0], network.NetworkResource)
        sortedList = sorted(list.resources,
                            key=lambda Network: Network.title,
                            reverse=True)
        self.assertEqual("private", sortedList[0].title)

    def test_list_by_tenant(self):
        self.req.headers = fakes.create_header(None, None, self.project_id)
        list = self.controller.index(self.req)
        sortedList = sorted(list.resources,
                            key=lambda Network: Network.title,
                            reverse=True)
        self.assertIsInstance(sortedList[0], network.NetworkResource)
      #  self.assertEqual("public", sortedList[0].title)

    def test_list_by_tenant_error(self):
        self.req.headers = fakes.create_header(None, None, "noexits")
        list = self.controller.index(self.req)
        self.assertIs(0, list.resources.__len__())

    def test_show_network(self):
        net = self.controller.show(self.req, self.public_network)
        self.assertEqual("public", net.title)

    def test_run_up_network(self):
        body = None
        out = None
        try:
            self.controller.run_action(self.req,
                                       self.public_network, body)
        except Exception as e:
            out = e
        self.assertIsInstance(out, exception.InvalidAction)

    def test_create_network_no_subnetwork(self):
        #Create
        parameters = {"occi.core.title": self.new_network_name}
        self.req.headers = fakes.create_header(parameters, None)
        try:
            self.controller.create(self.req)
        except Exception as e:
            out = e
        self.assertIsInstance(out, exception.Invalid)

    def test_create_delete_network_with_all(self):
        list1 = self.controller.index(self.req)
        ip_version = 4
        cidr = "12.0.0.1/24"
        gateway = "12.0.0.3"
        #Create
        parameters ={"occi.core.title": self.new_network_name,
                    "org.openstack.network.ip_version": ip_version,
                    "occi.network.address": cidr,
                    "occi.network.gateway": gateway,
                     }
        categories = {network.NetworkResource.kind,
                      network.ip_network}
        self.req.headers = fakes.create_header_occi(parameters, categories)
        ret = self.controller.create(self.req)
        net = ret.resources.pop()
        self.assertEqual(self.new_network_name, net.title)
        self.req.headers.pop("X-OCCI-Attribute")
        list2 = self.controller.index(self.req)
        self.assertEqual(list1.resources.__len__() + 1,
                         list2.resources.__len__())

         # Delete
        #id = 'c9b50445-9d6f-402a-91cd-d7c323402f96'
        response = self.controller.delete(self.req, net.id)
        self.assertIsInstance(response, list)
        list3 = self.controller.index(self.req)
        self.assertEqual(list1.resources.__len__(), list3.resources.__len__())


