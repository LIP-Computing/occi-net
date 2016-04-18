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
import mock

from ooi import exception
from ooi.api import helpers
from ooi.api import network
from ooi.occi.infrastructure import network as occi_network
from ooi.tests import base
from ooi.tests import fakes_neutron as fakes


class TestNetworkController(base.TestController):

    def setUp(self):
        super(TestNetworkController, self).setUp()
        self.controller = network.Controller(None)

    @mock.patch.object(helpers.OpenStackNet, "list_resources")
    def test_index(self, m_index):
        test_networks = [
            fakes.networks[fakes.tenants["bar"]["id"]],
            fakes.networks[fakes.tenants["foo"]["id"]]
        ]
        req = fakes.create_req_test(None, None)
        for nets in test_networks:
            ooi_net = helpers.OpenStackNet._build_networks(nets)
            m_index.return_value = ooi_net
            result = self.controller.index(req)
            expected = self.controller._get_network_resources(ooi_net)
            self.assertEqual(result.resources.__len__(),
                             expected.__len__())
            # self.assertEqual(result.resources, expected)
            m_index.assert_called_with(req, 'networks', None)

    @mock.patch.object(helpers.OpenStackNet, "get_network_details")
    def test_show(self, m_network):
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
        for net in test_networks:
            ret = self.controller.show(None, net["id"])
            self.assertIsInstance(ret, occi_network.NetworkResource)

    @mock.patch.object(helpers.OpenStackNet, "create_network")
    def test_create(self, m):
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
        schema1 = occi_network.NetworkResource.kind.scheme
        # m_network.return_value = {"id":"xxx"}
        for net in test_networks:
            parameters = {"occi.core.title": net["name"],
                          "org.openstack.network.ip_version": 4,
                          "occi.network.address": "0.0.0.0",
                          }
            categories = {occi_network.NetworkResource.kind}
            req = fakes.create_req_test_occi(parameters, categories)
            ret = self.controller.create(req)
            self.assertIsInstance(ret, occi_network.NetworkResource)

    @mock.patch.object(helpers.OpenStackNet, "create_resource")
    def test_create_Error(self, m):
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
        schema1 = occi_network.NetworkResource.kind.scheme
        net = test_networks[0]
        schemes = {schema1: net}
        parameters = {"occi.core.title": "name",
                      }
        req = fakes.create_req_test(parameters, schemes)

        self.assertRaises(exception.Invalid, self.controller.create, req)

    @mock.patch.object(helpers.OpenStackNet, "delete_network")
    def test_delete(self, m_network):
        m_network.return_value = []
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
        # schema1 = network.Network.scheme
        for net in test_networks:
            ret = self.controller.delete(None, net["id"])
            self.assertEquals(ret, [])
            self.assertEqual(ret.__len__(), 0)

    def test_get_network_resources(self):
        test_networks = fakes.networks[fakes.tenants["foo"]["id"]]
        subnet = fakes.subnets
        for net in test_networks:
            net["subnet_info"] = subnet[0]
        ooi_net = helpers.OpenStackNet._build_networks(test_networks)
        ret = self.controller._get_network_resources(ooi_net)
        self.assertIsInstance(ret, list)
        self.assertIsNot(ret.__len__(), 0)
        for net_ret in ret:
            self.assertIsInstance(net_ret, occi_network.NetworkResource)

    def test_filter_attributes(self):
        parameters ={"occi.core.title": 'name',
                    "org.openstack.network.ip_version": '777',
                    "occi.network.address": '77777',
                    "occi.network.gateway": '7777',
                     }
        categories = {occi_network.NetworkResource.kind}
        req = fakes.create_req_test_occi(parameters, categories)
        occi_scheme = {
            "category": occi_network.NetworkResource.kind,
            "optional_mixins": [
                occi_network.ip_network,
            ]
        }
        ret = network.process_parameters(req, occi_scheme)
        self.assertIsNotNone(ret)
        self.assertEqual(parameters, ret)

    def test_filter_attributes_empty(self):
        categories = {occi_network.NetworkResource.kind}
        req = fakes.create_req_test_occi(None, categories)
        occi_scheme = {
            "category": occi_network.NetworkResource.kind,
            "optional_mixins": [
                occi_network.ip_network,
            ]
        }
        attributes = network.process_parameters(req, occi_scheme)
        self.assertIsNone(attributes)
