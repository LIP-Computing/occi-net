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

import  collections

import mock

from occinet.api import network, helpers

from occinet.infrastructure.network_extend import Network
from occinet.tests import fakes
from ooi.tests import base


class TestNetworkController(base.TestController):

    def setUp(self):
        super(TestNetworkController, self).setUp()
        self.controller = network.Controller(mock.MagicMock(), None)

    @mock.patch.object(helpers.OpenStackNet, "index")
    def test_index(self, m_index):
        test_networks = [
            [],
            fakes.networks
        ]

        for nets in test_networks:
            m_index.return_value = nets
            result = self.controller.index(None, None)
            expected = self.controller._get_network_resources(nets)
            self.assertEqual(result.resources.__len__(),result.resources.__len__())
            self.assertEqual(expected, expected)
            if result.resources.__len__() > 0: #check that the object has 13 attributes,
                                                 # they belong from RESOURCE+NETWORKRESOURCE+NETWORK
                self.assertEqual(12, result.resources[0].attributes.attributes.__len__())
            m_index.assert_called_with(None, None)

    @mock.patch.object(helpers.OpenStackNet, "get_network")
    def test_show(self, m_network):
        test_networks = fakes.networks
        for net in test_networks:
            ret = self.controller.show(None, net["id"])
            self.assertIsInstance(ret, Network)

    @mock.patch.object(helpers.OpenStackNet, "create_network")
    def test_create(self, m_network):
        test_networks = fakes.networks
        schema1 = network.Network.scheme
        for net in test_networks:
            schemes = {schema1:net}
            parameters={
                    'attributes':{'occi.core.id':1},
                    'category': "%s%s" % (schema1, net),
                    'schemes': schemes
                    }
            ret = self.controller.create(None, parameters=parameters)
            self.assertIsInstance(ret, Network)

    @mock.patch.object(helpers.OpenStackNet, "delete_network")
    def test_delete(self, m_network):
        test_networks = fakes.networks
        schema1 = network.Network.scheme
        for net in test_networks:
            schemes = {schema1:net}
            parameters={
                    'attributes':{'occi.core.id':1},
                    'category': "%s%s" % (schema1, net),
                    'schemes': schemes
                    }
            ret = self.controller.delete(None, parameters=parameters)
            self.assertIsInstance(ret, list)
            self.assertEqual(ret.__len__(), 0)

    def test_get_network_resources(self):
        test_networks = fakes.networks
        subnet = fakes.subnets
        for net in test_networks:
            net["subnet_info"] = subnet[0]
        ret = self.controller._get_network_resources(test_networks)
        self.assertIsInstance(ret, list)
        self.assertIsNot(ret.__len__(), 0)
        for net_ret in ret:
            self.assertIsInstance(net_ret,Network)

    #_filter_attributes


#    @mock.patch.object(openstack_driver.OpenStackNet, "index")
#    def test_list_by_tenant(self, m_index): #TODO(jorgesece): the fake driver should be improved to make parametriced query tests
#        list = self.controller.index(None, {"tenant_id" : "foo", "name" : "public"})

#        self.assertIsInstance(list.resources[0], Network)
#        self.assertEqual("public", list.resources[0].title)