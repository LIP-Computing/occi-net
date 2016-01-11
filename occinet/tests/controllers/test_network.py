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
            fakes.networks[fakes.tenants["foo"]["id"]]
        ]

        for nets in test_networks:
            m_index.return_value = nets
            result = self.controller.index(None, None)
            expected = self.controller._get_network_resources(nets)
            self.assertEqual(result.resources.__len__(),result.resources.__len__())
            self.assertEqual(expected, expected)
            if result.resources.__len__() > 0: #check that the object has 9 attributes,
                                                 # they belong from RESOURCE+NETWORKRESOURCE+NETWORK
                self.assertEqual(9, result.resources[0].attributes.attributes.__len__())
            m_index.assert_called_with(None, None)

    @mock.patch.object(helpers.OpenStackNet, "get_network")
    def test_show(self, m_network):
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]
        ]
        for net in test_networks:
            ret = self.controller.show(None, net["id"])
            self.assertIsInstance(ret, Network)

    # @mock.patch.object(helpers.OpenStackNet, "create_network")
    # def test_create(self, m_network):
    #     test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
    #     cat1 = "network1"
    #     cat2 = "subnetwork1"
    #     cat3 = "subnetwork2"
    #     schema1 = network.Network.scheme
    #     schema2 = subnetwork.Subnetwork.scheme
    #     mixins = collections.Counter()
    #     mixins["%s%s" % (schema2, cat2)] += 1
    #     mixins["%s%s" % (schema2, cat3)] += 1
    #     schemes = {schema1:cat1, schema2: [cat2,cat3] }
    #     parameters={
    #                 'attributes':{'occi.core.id':1},
    #                 'category': "%s%s" % (schema1, cat1),
    #                 'mixins': mixins,
    #                 'schemes': schemes
    #                 }
    #
    #
    #     ret = self.controller.create(None, parameters=parameters)
    #     self.assertIsInstance(ret, Network)

    @mock.patch.object(helpers.OpenStackNet, "create_network")
    def test_create_one_mixin(self, m_network):
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
        cat1 = "network1"
        cat2 = "subnetwork1"
        schema1 = network.Network.scheme
        #schema2 = subnetwork.Subnetwork.scheme
        mixins = collections.Counter()
       #mixins["%s%s" % (schema2, cat2)] += 1
        schemes = { schema1:cat1 }
        parameters={
                    'attributes':{'occi.core.id':1},
                    'category': "%s%s" % (schema1, cat1),
                    'mixins': mixins,
                    'schemes': schemes
                    }

        ret = self.controller.create(None, parameters=parameters)
        self.assertIsInstance(ret, Network)


#    @mock.patch.object(openstack_driver.OpenStackNet, "index")
#    def test_list_by_tenant(self, m_index): #TODO(jorgesece): the fake driver should be improved to make parametriced query tests
#        list = self.controller.index(None, {"tenant_id" : "foo", "name" : "public"})

#        self.assertIsInstance(list.resources[0], Network)
#        self.assertEqual("public", list.resources[0].title)