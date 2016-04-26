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
import json
import uuid

import mock

from ooi.api import helpers
from ooi import exception
from ooi.tests import base
from ooi.tests import fakes_neutron as fakes
from ooi import utils


class TestNovaNetOpenStackHelper(base.TestCase):
    def setUp(self):
        super(TestNovaNetOpenStackHelper, self).setUp()
        self.version = "version foo bar baz"
        self.helper = helpers.OpenStackNovaNetwork(self.version)
        self.translation = {"networks": {"occi.core.title": "label",
                                         "occi.core.id": "id",
                                         "occi.network.address": "cidr",
                                         "occi.network.gateway": "gateway",
                                         "org.openstack.network.shared": "share_address",
                                         "X_PROJECT_ID": "tenant_id",
                                         }
                            }

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_make_get_request")
    def test_index(self, m):
        id = uuid.uuid4().hex
        resp = fakes.create_fake_json_resp({"networks": [{"id": id}]}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.index(None, None)
        self.assertEqual(id, ret[0]['id'])
        m.assert_called_with(None, "os-networks", None)

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_make_get_request")
    def test_get_network(self, m):
        id = uuid.uuid4().hex
        resp = fakes.create_fake_json_resp(
            {"network": {"status": "ACTIVE", "id": id}}, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.get_network_details(None, id)
        self.assertEqual("active", ret["state"])
        m.assert_called_with(None, "os-networks/%s" % id)

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_get_network2(self, m_t, m_rq):
        id = uuid.uuid4().hex
        address = uuid.uuid4().hex
        gateway = uuid.uuid4().hex
        label = "network11"
        tenant_id = uuid.uuid4().hex
        m_t.return_value = tenant_id
        resp = fakes.create_fake_json_resp(
            {"network": { "id": id, "label": label,
                          "cidr": address,
                          "gateway": gateway}}, 200
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_rq.return_value = req_mock
        ret = self.helper.get_network_details(None, id)
        self.assertEqual(id, ret["id"])
        self.assertEqual(address, ret["address"])
        self.assertEqual(gateway, ret["gateway"])
        self.assertEqual(label, ret["name"])
        m_rq.assert_called_with(None, method="GET",
                             path="%s/os-networks/%s" % (tenant_id, id),
                             query_string=None)

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_make_create_request")
    def test_create_net(self, m):
        name = "name_net"
        net_id = uuid.uuid4().hex
        state = "ACTIVE"
        project = "project_id"
        ip_version = 4
        cidr = "0.0.0.0"
        gate_way = "0.0.0.1"
        parameters = {"occi.core.title": name,
                      "occi.core.id": net_id,
                      "occi.network.address": cidr,
                      "occi.network.gateway": gate_way
                      }
        resp = fakes.create_fake_json_resp(
            {"network": {"id": net_id,
                         "label": name,
                         "cidr": cidr,
                         "gateway": gate_way}}, 201
        )
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.create_network(None, parameters)
        self.assertEqual(net_id, ret["id"])
        self.assertEqual(cidr, ret['address'])
        self.assertEqual(gate_way, ret['gateway'])
        param = utils.translate_parameters(
            self.translation["networks"], parameters)
        m.assert_called_with(None, "os-networks", param)

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_make_delete_request")
    def test_delete_network(self, m):
        id = uuid.uuid4().hex
        resp = fakes.create_fake_json_resp({"network": []}, 204)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m.return_value = req_mock
        ret = self.helper.delete_network(None, id)
        self.assertEqual(ret, [])
        m.assert_called_with(None, "os-networks", id)

    @mock.patch.object(helpers.OpenStackNeutron, "create_resource")
    def test_create_port(self, m_create):
        ip = '22.0.0.1'
        net_id = uuid.uuid4().hex
        mac = '890234'
        device_id = uuid.uuid4().hex
        p = {"network_id": net_id, 'device_id': device_id,
             "fixed_ips": [{"ip_address": ip}],
             "mac_address": mac, "status": "ACTIVE"
             }
        m_create.return_value = p
        ret = self.helper.create_port(None, {'sa': 1})
        self.assertEqual(device_id, ret['compute_id'])
        self.assertEqual(ip, ret['ip'])
        self.assertEqual(net_id, ret['network_id'])
        self.assertEqual(mac, ret['mac'])


    # @mock.patch.object(helpers.OpenStackNeutron, "_get_public_network")
    # @mock.patch.object(helpers.OpenStackNeutron, "list_resources")
    # @mock.patch.object(helpers.OpenStackNeutron, "_add_floating_ip")
    # def test_assign_floating_ip(self, m_add, m_list, m_get_net):
    #     compute_id = uuid.uuid4().hex
    #     net_id = uuid.uuid4().hex
    #     param_occi = {'occi.core.target': net_id,
    #                   'occi.core.source': compute_id
    #                   }
    #     f_id = uuid.uuid4().hex
    #     ip = '0.0.0.1'
    #     port = {'id': 11, 'network_id': net_id,
    #             'device_owner': 'nova'}
    #     param = {'device_id': compute_id}
    #     m_get_net.return_value = net_id
    #     m_list.return_value = [port]
    #     m_add.return_value = {"id": f_id,
    #                           'floating_ip_address': ip,
    #                           'floating_network_id': '84'}
    #     ret = self.helper.assign_floating_ip(None, param_occi)
    #     self.assertEqual(net_id, ret['network_id'])
    #     self.assertEqual(ip, ret['ip'])
    #     m_list.assert_called_with(None, 'ports', param)
    #     m_add.assert_called_with(None, net_id, port['id'])
    #
    # @mock.patch.object(helpers.OpenStackNeutron, "_get_public_network")
    # @mock.patch.object(helpers.OpenStackNeutron, "_remove_floating_ip")
    # def test_release_floating_ip(self, m_add, m_get_net):
    #     ip = '22.0.0.1'
    #     net_id = 'PUBLIC'
    #
    #     m_get_net.return_value = net_id
    #     m_add.return_value = []
    #     ret = self.helper.release_floating_ip(None, ip)
    #     self.assertEqual([], ret)
    #     m_add.assert_called_with(None, net_id, ip)
    #
    # @mock.patch.object(helpers.OpenStackNeutron, "create_resource")
    # def test_create_port(self, m_create):
    #     ip = '22.0.0.1'
    #     net_id = uuid.uuid4().hex
    #     mac = '890234'
    #     device_id = uuid.uuid4().hex
    #     p = {"network_id": net_id, 'device_id': device_id,
    #          "fixed_ips": [{"ip_address": ip}],
    #          "mac_address": mac, "status": "ACTIVE"
    #          }
    #     m_create.return_value = p
    #     ret = self.helper.create_port(None, {'sa': 1})
    #     self.assertEqual(device_id, ret['compute_id'])
    #     self.assertEqual(ip, ret['ip'])
    #     self.assertEqual(net_id, ret['network_id'])
    #     self.assertEqual(mac, ret['mac'])
    #
    # @mock.patch.object(helpers.OpenStackNeutron, "list_resources")
    # @mock.patch.object(helpers.OpenStackNeutron, "delete_resource")
    # def test_delete_port(self, m_delete, m_list):
    #     port_id = uuid.uuid4().hex
    #     p = [{'id': port_id}]
    #     m_list.return_value = p
    #     m_delete.return_value = []
    #     ret = self.helper.delete_port(None, None)
    #     self.assertEqual([], ret)
    #
    # @mock.patch.object(helpers.OpenStackNeutron, "list_resources")
    # def test_list_port_not_found(self, m_list):
    #     m_list.return_value = []
    #     self.assertRaises(exception.LinkNotFound,
    #                       self.helper.delete_port,
    #                       None,
    #                       None)
    #
    #    @mock.patch.object(helpers.OpenStackNeutron, "list_resources")
    # def test_get_public_network(self, m):
    #     public_id = uuid.uuid4().hex
    #     m.return_value = [{"id": public_id}]
    #     ret = self.helper._get_public_network(None)
    #     att_public = {"router:external": True}
    #     self.assertEqual(public_id, ret)
    #     m.assert_called_with(None, 'networks', att_public)
    #
    # @mock.patch.object(helpers.OpenStackNeutron, "create_resource")
    # def test_add_floating_ip(self, m):
    #     port_id = uuid.uuid4().hex
    #     public_net = uuid.uuid4().hex
    #     f_ip = uuid.uuid4().hex
    #     ip = '0.0.0.1'
    #     m.return_value = {"id": f_ip,
    #                       'floating_ip_address': ip}
    #     ret = self.helper._add_floating_ip(None, public_net, port_id)
    #     attributes_port = {
    #         "floating_network_id": public_net,
    #         "port_id": port_id
    #     }
    #     self.assertEqual(f_ip, ret['id'])
    #     self.assertEqual(ip, ret['floating_ip_address'])
    #     m.assert_called_with(None, 'floatingips', attributes_port)
    #
    # @mock.patch.object(helpers.OpenStackNeutron, "delete_resource")
    # @mock.patch.object(helpers.OpenStackNeutron, "list_resources")
    # def test_remove_floating_ip(self, m_list, m_del):
    #     ip = '1.0.0.0'
    #     public_net = uuid.uuid4().hex
    #     f_ip = uuid.uuid4().hex
    #     m_list.return_value = [{'id': f_ip}]
    #     m_del.return_value = []
    #     ret = self.helper._remove_floating_ip(None, public_net, ip)
    #     attributes_port = {
    #         "floating_network_id": public_net,
    #         "floating_ip_address": ip
    #     }
    #     self.assertEqual([], ret)
    #     m_list.assert_called_with(None, 'floatingips', attributes_port)
    #     m_del.assert_called_with(None, 'floatingips', f_ip)

