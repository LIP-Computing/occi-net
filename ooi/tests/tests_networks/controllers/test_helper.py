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
import json

import mock

from ooi.api import helpers
from ooi.tests import base
from ooi.tests.tests_networks import fakes
from ooi import utils


class TestNetOpenStackHelper(base.TestCase):
    def setUp(self):
        super(TestNetOpenStackHelper, self).setUp()
        self.version = "version foo bar baz"
        self.helper = helpers.OpenStackNet(self.version)
        self.translation = {"networks": {"occi.core.title": "name",
                                        "occi.core.id": "network_id",
                                        "occi.network.state": "status",
                                        "X_PROJECT_ID": "tenant_id",
                                        },
                            "subnets": {"occi.core.id": "network_id",
                                       "org.openstack.network.ip_version": "ip_version",
                                       "occi.network.address": "cidr",
                                       "occi.network.gateway":
                                           "gateway_ip"
                                       }
                            }

    @mock.patch.object(helpers.OpenStackNet, "_make_get_request")
    def test_index(self, m):
        resp = fakes.create_fake_json_resp({"networks": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.list_resources(None,'networks', None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None, "/networks", None)

    @mock.patch.object(helpers.OpenStackNet, "_get_req")
    def test_index2(self, m):
        resp = fakes.create_fake_json_resp({"networks": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.list_resources(None,'networks', None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None, method="GET",
                             path="/networks", query_string=None)

    @mock.patch.object(helpers.OpenStackNet, "_make_get_request")
    def test_index3(self, m):
        resp = fakes.create_fake_json_resp({"networks": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.index(None, None)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None, "/networks", None)

    @mock.patch.object(helpers.OpenStackNet, "_make_get_request")
    def test_get_network(self, m):
        resp = fakes.create_fake_json_resp(
            {"network": {"status": "ACTIVE"}}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_network_details(None, 1)
        self.assertEqual("ACTIVE", ret["status"])
        m.assert_called_with(None, "/networks/%s" % 1)

    @mock.patch.object(helpers.OpenStackNet, "_get_req")
    def test_get_network2(self, m):
        resp = fakes.create_fake_json_resp(
            {"network": {"status": "ACTIVE"}}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_network_details(None, 1)
        self.assertEqual("ACTIVE", ret["status"])
        m.assert_called_with(None, method="GET",
                             path="/networks/1", query_string=None)

    @mock.patch.object(helpers.OpenStackNet, "_make_get_request")
    def test_get_subnetwork(self, m):
        resp = fakes.create_fake_json_resp(
            {"subnet": ["FOO"]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_resource(None, 'subnets', 1)
        self.assertEqual(["FOO"], ret)
        m.assert_called_with(None, "/subnets/%s" % 1)

    @mock.patch.object(helpers.OpenStackNet, "_make_get_request")
    def test_get_network_with_subnet(self, m):
        resp = fakes.create_fake_json_resp(
            {"network": {"status": "ACTIVE", "subnets": [2]},
             "subnet": ["FOO"]}, 200
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_network_details(None, 1)
        self.assertEqual("ACTIVE", ret["status"])
        self.assertEqual([2], ret["subnets"])
        self.assertEqual(["FOO"], ret["subnet_info"])
        m.assert_called_with(req_mock, "/subnets/2")

    @mock.patch.object(helpers.OpenStackNet, "_get_req")
    def test_get_network_with_subnet2(self, m):
        resp = fakes.create_fake_json_resp(
            {"network": {"status": "ACTIVE", "subnets": [2]},
             "subnet": ["FOO"]}, 200
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_network_details(None, 1)
        self.assertEqual("ACTIVE", ret["status"])
        self.assertEqual([2], ret["subnets"])
        self.assertEqual(["FOO"], ret["subnet_info"])
        m.assert_called_with(req_mock, method="GET",
                             path="/subnets/2", query_string=None)

    @mock.patch.object(helpers.OpenStackNet, "_make_create_request")
    def test_create_only_network(self, m):
        name = "name_net"
        net_id = 1
        state = "ACTIVE"
        project = "project_id"
        parameters = {"occi.core.title": name,
                      "occi.core.id": net_id,
                      "occi.network.state": state,
                      "project": project,
                      }
        resp = fakes.create_fake_json_resp(
            {"network": {"network_id": net_id}}, 201)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.create_resource(None, 'networks', parameters)
        self.assertEqual(net_id, ret["network_id"])
        m.assert_called_with(None, "networks", parameters)

    @mock.patch.object(helpers.OpenStackNet, "_make_create_request")
    def test_create_resource_net_subnet(self, m):
        name = "name_net"
        net_id = 1
        state = "ACTIVE"
        project = "project_id"
        ip_version = "IPv4"
        cidr = "0.0.0.0"
        gate_way = "0.0.0.1"
        subnet_id = 11
        parameters = {"occi.core.title": name,
                      "occi.core.id": net_id,
                      "occi.network.state": state,
                      "X_PROJECT_ID": project,
                      "occi.network.ip_version": ip_version,
                      "occi.networkinterface.address": cidr,
                      "occi.networkinterface.gateway": gate_way
                      }
        resp = fakes.create_fake_json_resp(
            {"network": {"id": net_id},
             "subnet": {"id": subnet_id}}, 201
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.create_resource(None,'networks', parameters)
        self.assertEqual(net_id, ret["id"])
        ret2 = self.helper.create_resource(None,'subnets', parameters)
        self.assertEqual(subnet_id, ret2["id"])
        m.assert_called_with(None, "subnets", parameters)

    @mock.patch.object(helpers.OpenStackNet, "_get_req")
    def test_create_resource_net_subnet_req(self, m):
        name = "name_net"
        net_id = 1
        state = "ACTIVE"
        project = "project_id"
        ip_version = 4
        cidr = "0.0.0.0"
        gate_way = "0.0.0.1"
        subnet_id = 11
        parameters = {"occi.core.title": name,
                      "occi.core.id": net_id,
                      "occi.network.state": state,
                      "X_PROJECT_ID": project,
                      "org.openstack.network.ip_version": ip_version,
                      "occi.network.address": cidr,
                      "occi.network.gateway": gate_way
                      }
        resp = fakes.create_fake_json_resp(
            {"network": {"id": net_id},
             "subnet": {"id": subnet_id}}, 201
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.create_resource(None,'networks', parameters)
        self.assertEqual(net_id, ret["id"])
        ret2 = self.helper.create_resource(None,'subnets', parameters)
        self.assertEqual(subnet_id, ret2["id"])
        m.assert_called_with(None,
                             path="/subnets",
                             content_type="application/json",
                             body=json.dumps(utils.make_body(
                                 "subnet", parameters)),
                             method="POST")

    @mock.patch.object(helpers.OpenStackNet, "_make_put_request")
    def test_add_router_interface(self, m):
        router_id = 1
        subnet_id = 11
        port_id = 111
        resp = fakes.create_fake_json_resp(
            {"port_id": port_id, "subnet_id": subnet_id}, 201
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper._add_router_interface(None, router_id, subnet_id)
        self.assertEqual(port_id, ret["port_id"])
        self.assertEqual(subnet_id, ret["subnet_id"])
        path = "/routers/%s/add_router_interface" % router_id
        param = {"subnet_id": subnet_id}
        m.assert_called_with(None, path, param)

    @mock.patch.object(helpers.OpenStackNet, "_make_put_request")
    def test_remove_router_interface(self, m):
        router_id = 1
        subnet_id = 11
        port_id = 111
        resp = fakes.create_fake_json_resp(
            {"port_id": port_id, "subnet_id": subnet_id}, 201
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper._remove_router_interface(None, router_id, port_id)
        self.assertEqual(port_id, ret["port_id"])
        self.assertEqual(subnet_id, ret["subnet_id"])
        path = "/routers/%s/remove_router_interface" % router_id
        param = {"port_id": port_id}
        m.assert_called_with(None, path, param)

    @mock.patch.object(helpers.OpenStackNet, "list_resources")
    def test_get_public_network(self, m):
        public_id = 111
        m.return_value = [{"id": 111}]
        ret = self.helper._get_public_network(None)
        att_public = {"router:external": True}
        self.assertEqual(public_id, ret)
        m.assert_called_with(None, 'networks', att_public)

    @mock.patch.object(helpers.OpenStackNet, "create_resource")
    def test_add_floating_ip(self, m):
        port_id = 1
        public_net = 111
        f_ip = 33
        ip = '0.0.0.1'
        m.return_value = {"id": f_ip,
                          'floating_ip_address': ip}
        ret = self.helper._add_floating_ip(None, public_net, port_id)
        attributes_port = {
            "floating_network_id": public_net,
            "port_id": port_id
        }
        self.assertEqual(f_ip, ret['id'])
        self.assertEqual(ip, ret['floating_ip_address'])
        m.assert_called_with(None, 'floatingips', attributes_port)

    @mock.patch.object(helpers.OpenStackNet, "delete_resource")
    @mock.patch.object(helpers.OpenStackNet, "list_resources")
    def test_add_floating_ip(self, m_list, m_del):
        port_id = 1
        public_net = 111
        f_ip = 33
        m_list.return_value = [{'id':f_ip}]
        m_del.return_value = []
        ret = self.helper._remove_floating_ip(None, public_net, port_id)
        attributes_port = {
            "floating_network_id": public_net,
            "port_id": port_id
        }
        self.assertEqual([], ret)
        m_list.assert_called_with(None, 'floatingips', attributes_port)
        m_del.assert_called_with(None, 'floatingips', f_ip)

    @mock.patch.object(helpers.OpenStackNet, "create_resource")
    @mock.patch.object(helpers.OpenStackNet, "list_resources")
    @mock.patch.object(helpers.OpenStackNet, "_add_router_interface")
    def test_create_full_network(self, add_if, list_net, cre_net):
        name = "name_net"
        net_id = 1
        subnet_id = 11
        router_id = 111
        public_net = 1111
        state = "ACTIVE"
        project = "project_id"
        ip_version = 4
        cidr = "0.0.0.0/24"
        gate_way = "0.0.0.1"
        parameters = {"occi.core.title": name,
                      "occi.core.id": net_id,
                      "occi.network.state": state,
                      "X_PROJECT_ID": project,
                      "org.openstack.network.ip_version": ip_version,
                      "occi.network.address": cidr,
                      "occi.network.gateway": gate_way
                      }
        cre_net.side_effect = [{'id': net_id},
                               {"id": subnet_id,
                                "cidr": cidr,
                                "gateway_ip": gate_way},
                               {"id": router_id},
                               {"id": 0}]
        list_net.return_value = [{'id': public_net}]
        ret = self.helper.create_network(None, parameters)
        self.assertEqual(net_id, ret["id"])
        param = utils.translate_parameters(
            self.translation["networks"], parameters)
        self.assertEquals((None,'networks',
                           param),
                          cre_net.call_args_list[0][0])
        param_subnet = utils.translate_parameters(
            self.translation["subnets"], parameters)
        param_subnet['network_id'] = net_id
        self.assertEquals((None,'subnets',
                           param_subnet),
                          cre_net.call_args_list[1][0])
        self.assertEquals((None,'routers',
                           {'external_gateway_info':{'network_id':public_net}}),
                          cre_net.call_args_list[2][0])
        add_if.assert_called_with(None, router_id, subnet_id)
        self.assertEqual(subnet_id, ret["subnet_info"]['id'])
        self.assertEqual(cidr, ret["subnet_info"]['cidr'])
        self.assertEqual(gate_way, ret["subnet_info"]['gateway_ip'])

    @mock.patch.object(helpers.OpenStackNet, "delete_resource")
    @mock.patch.object(helpers.OpenStackNet, "list_resources")
    @mock.patch.object(helpers.OpenStackNet, "_remove_router_interface")
    def test_delete_network(self, m_if, m_list, m_del):
        net_id = 11
        router_id = 33
        m_del.side_effect = [{0},
                             {0},
                             {0},
                             ]
        port1 = {'id': 1,
                 'device_owner': 'network:router_interface',
                 'device_id': router_id
                 }
        port2 = {'id': 2, 'device_owner': 'nova'}
        m_list.return_value = [port1, port2]
        m_del.side_effect = [{0},{0},[]]
        m_if.return_value = []
        ret = self.helper.delete_network(None, net_id)
        self.assertEqual(ret, [])
        self.assertEquals((None, 'routers',
                           port1['device_id']),
                          m_del.call_args_list[0][0])
        self.assertEquals((None, 'ports',
                           port2['id']),
                          m_del.call_args_list[1][0])
        self.assertEquals((None, 'networks',
                           net_id),
                          m_del.call_args_list[2][0])

    @mock.patch.object(helpers.OpenStackNet, "_make_delete_request")
    def test_delete_network_resource_make_mock(self, m):
        resp = fakes.create_fake_json_resp({"network": []}, 204)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.delete_resource(None,'networks', 1)
        self.assertEqual(ret, [])
        m.assert_called_with(None, "/networks", 1)

    @mock.patch.object(helpers.OpenStackNet, "_get_req")
    def test_response_delete_network_resource(self, m):
        resp = fakes.create_fake_json_resp({"network": []}, 204)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        id = 1
        ret = self.helper.delete_resource(None,'networks', id)
        self.assertEqual(ret, [])
        m.assert_called_with(None, method="DELETE",
                             path="/networks/1")

    # TODO(JORGESECE): add tests to:
    # assign_floating_ip
    # release_floating_ip