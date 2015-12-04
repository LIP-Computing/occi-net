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

import mock

from occinet.api import network
from ooi.tests import base

from occinet.drivers.openstack import openstack_driver
from occinet.tests import fakes


class TestNetworkController(base.TestController):

    def setUp(self):
        super(TestNetworkController, self).setUp()
        self.controller = network.Controller(mock.MagicMock(), None)

    @mock.patch.object(openstack_driver.OpenStackNet, "index")
    def test_index(self, m_index):
        test_networks = [
            [],
            fakes.networks[fakes.tenants["foo"]["id"]]
        ]

        for nets in test_networks:
            m_index.return_value = nets
            result = self.controller.index(None, None)
            expected = self.controller._get_network_resources(nets)
            self.assertEqual(expected, result.resources)
            m_index.assert_called_with(None, None)

    @mock.patch.object(openstack_driver.OpenStackNet, "index")
    def test_list_by_tenant(self, m_index): #TODO(jorgesece): the fake driver should be improved to make parametriced query tests
        list = self.controller.index(None, {"tenant_id" : "foo", "name" : "public"})

        self.assertIsInstance(list.resources[0], network_occi.NetworkResource)
        self.assertEqual("public", list.resources[0].title)