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
import uuid
import webob

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
        self.helper = helpers.OpenStackNovaNetwork(None, self.version)
        self.translation = {"networks": {"occi.core.title": "label",
                                         "occi.core.id": "id",
                                         "occi.network.address": "cidr",
                                         "occi.network.gateway": "gateway",
                                         "org.openstack.network.shared": "share_address",
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
                             path="/%s/os-networks/%s" % (tenant_id, id),
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
        self.assertRaises(exception.NotImplemented,
                          self.helper.create_network,
                          None,
                          parameters)

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_make_delete_request")
    def test_delete_network(self, m):
        id = uuid.uuid4().hex
        self.assertRaises(exception.NotImplemented,
                          self.helper.delete_network, None,
                          id)

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_make_create_request")
    def test_create_port(self, m_create):
        ip = '22.0.0.1'
        net_id = uuid.uuid4().hex
        mac = '890234'
        device_id = uuid.uuid4().hex
        p = {"interfaceAttachment": {"net_id": net_id,
             "fixed_ips": [{"ip_address": ip}],
             "mac_addr": mac, "port_state": "ACTIVE"
             }}
        response = fakes.create_fake_json_resp(p, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = response
        m_create.return_value = req_mock
        ret = self.helper.create_port(None, {'occi.core.source': device_id})
        self.assertEqual(device_id, ret['compute_id'])
        self.assertEqual(ip, ret['ip'])
        self.assertEqual(net_id, ret['network_id'])
        self.assertEqual(mac, ret['mac'])

    @mock.patch.object(helpers.OpenStackNovaNetwork, "_get_ports")
    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_make_delete_request")
    def test_delete_port(self, m_delete, m_ports):
        ip = '22.0.0.1'
        net_id = uuid.uuid4().hex
        mac = '890234'
        device_id = uuid.uuid4().hex
        port_id = uuid.uuid4().hex
        iface = {'compute_id': device_id,
                 'mac': mac}
        p = [{"net_id": net_id,
              "fixed_ips": [{"ip_address": ip}],
              "mac_addr": mac, "port_id": port_id
              }]
        m_ports.return_value = p
        response = fakes.create_fake_json_resp({}, 202)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = response
        m_delete.return_value = req_mock
        ret = self.helper.delete_port(None, iface)
        self.assertEqual([], ret)

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_associate_floating_ip(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        net_id = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        pool = uuid.uuid4().hex
        params = {"occi.core.source": device_id,
                  "occi.core.target": net_id}
        resp = fakes.create_fake_json_resp(
            {"floating_ip": {"ip": ip, "pool": pool}},
            202
        )
        req_all = mock.MagicMock()
        req_all.get_response.return_value = resp
        resp_ass = fakes.create_fake_json_resp({}, 202)
        req_ass = mock.MagicMock()
        req_ass.get_response.return_value = resp_ass
        m_req.side_effect =[req_all,
                            req_ass]
        ret = self.helper.assign_floating_ip(None, params)
        self.assertIsNotNone(ret)
        self.assertEqual(net_id, ret['network_id'])
        self.assertEqual(device_id, ret['compute_id'])
        self.assertEqual(ip, ret['ip'])
        self.assertEqual(pool, ret['pool'])

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_associate_associate_err(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        net_id = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        pool = uuid.uuid4().hex
        params = {"occi.core.source": device_id,
                  "occi.core.target": net_id}
        resp = fakes.create_fake_json_resp(
            {"floating_ip": {"ip": ip, "pool": pool}},
            202
        )
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp_ass = fakes.create_fake_json_resp(
            fault,
            500
        )
        req_all = mock.MagicMock()
        req_all.get_response.return_value = resp
        req_ass = mock.MagicMock()
        req_ass.get_response.return_value = resp_ass
        m_req.side_effect =[req_all,
                            req_ass]
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.assign_floating_ip,
                          None,
                          params)

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_associate_all_err(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        net_id = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        pool = uuid.uuid4().hex
        params = {"occi.core.source": device_id,
                  "occi.core.target": net_id}
        fault = {"computeFault": {"message": "bad", "code": 500}}
        resp = fakes.create_fake_json_resp(
            fault,
            500
        )
        req_all = mock.MagicMock()
        req_all.get_response.return_value = resp
        m_req.side_effect =[req_all
                            ]
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.assign_floating_ip,
                          None,
                          params)

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_floating_ip_release(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        mac = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        iface = {'server_id': device_id,
                 'mac': mac,
                 'ip': ip
                 }
        resp = fakes.create_fake_json_resp(None, 202)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_req.return_value = req_mock
        ret = self.helper.release_floating_ip(None, iface)
        self.assertIsNone(ret)

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_floating_ip_release_err(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        mac = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        iface = {'server_id': device_id,
                 'mac': mac,
                 'ip': ip
                 }
        resp = fakes.create_fake_json_resp(None, 204)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_req.return_value = req_mock
        self.assertRaises(webob.exc.HTTPInternalServerError,
                          self.helper.release_floating_ip,
                          None,
                          iface)

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_get_network_id(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        mac = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        net_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        p = {"interfaceAttachments": [{"net_id": net_id,
             "fixed_ips": [{"ip_address": ip}],
             "mac_addr": mac, "port_state": "ACTIVE"
             }]}
        resp = fakes.create_fake_json_resp(p, 200)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_req.return_value = req_mock
        ret = self.helper.get_network_id(None, mac, device_id)
        self.assertEqual(net_id, ret)

    @mock.patch.object(helpers.OpenStackNovaNetwork,
                       "_get_req")
    @mock.patch.object(helpers.BaseHelper, "tenant_from_req")
    def test_get_network_id_empty(self, m_ten, m_req):
        m_ten.return_value = uuid.uuid4().hex
        mac = uuid.uuid4().hex
        device_id = uuid.uuid4().hex
        net_id = uuid.uuid4().hex
        ip = uuid.uuid4().hex
        p = {"interfaceAttachments": []}
        resp = fakes.create_fake_json_resp(p, 204)
        req_mock = mock.MagicMock()
        req_mock.get_response.return_value = resp
        m_req.return_value = req_mock
        self.assertRaises(exception.NetworkNotFound,
                          self.helper.get_network_id,
                          None,
                          mac,
                          device_id)


    # class TestOpenStackHelperNetReqs(base.TestCase):
    #     def setUp(self):
    #         super(TestOpenStackHelperNetReqs, self).setUp()
    #         self.version = "version foo bar baz"
    #         self.helper = helpers.OpenStackNovaNetwork(mock.MagicMock(), self.version)
    #     def _build_req(self, tenant_id, **kwargs):
    #
    #         environ = {"HTTP_X_PROJECT_ID": tenant_id}
    #         return webob.Request.blank("/whatever", environ=environ, **kwargs)
    #
    #     def test_get_os_floating_ip_allocate(self):
    #         tenant = fakes.tenants["foo"]
    #         req = self._build_req(tenant["id"])
    #         pool = "foo"
    #         body = {"pool": pool}
    #         path = "/%s/os-floating-ips" % tenant["id"]
    #         os_req = self.helper._allocate_floating_ip(req, pool)
    #         self.assertExpectedReq("POST", path, body, os_req)
#
#     def test_get_os_floating_ip_allocate_no_pool(self):
#         tenant = fakes.tenants["foo"]
#         req = self._build_req(tenant["id"])
#         pool = None
#         body = {"pool": pool}
#         path = "/%s/os-floating-ips" % tenant["id"]
#         os_req = self.helper._get_floating_ip_allocate_req(req, pool)
#         self.assertExpectedReq("POST", path, body, os_req)
#
#     def test_get_os_floating_ip_release(self):
#         tenant = fakes.tenants["foo"]
#         req = self._build_req(tenant["id"])
#         ip = uuid.uuid4().hex
#         path = "/%s/os-floating-ips/%s" % (tenant["id"], ip)
#         os_req = self.helper._get_floating_ip_release_req(req, ip)
#         self.assertExpectedReq("DELETE", path, "", os_req)
#
#     def test_get_os_associate_floating_ip(self):
#         tenant = fakes.tenants["foo"]
#         req = self._build_req(tenant["id"])
#         server = uuid.uuid4().hex
#         ip = "192.168.0.20"
#         body = {"addFloatingIp": {"address": ip}}
#         path = "/%s/servers/%s/action" % (tenant["id"], server)
#         os_req = self.helper._get_associate_floating_ip_req(req, server, ip)
#         self.assertExpectedReq("POST", path, body, os_req)
#
#     def test_get_os_remove_floating_ip(self):
#         tenant = fakes.tenants["foo"]
#         req = self._build_req(tenant["id"])
#         server = uuid.uuid4().hex
#         ip = "192.168.0.20"
#         body = {"removeFloatingIp": {"address": ip}}
#         path = "/%s/servers/%s/action" % (tenant["id"], server)
#         os_req = self.helper._get_remove_floating_ip_req(req, server, ip)
#         self.assertExpectedReq("POST", path, body, os_req)



