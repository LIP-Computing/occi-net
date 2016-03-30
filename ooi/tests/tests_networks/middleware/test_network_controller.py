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

from ooi.api.networks import network
from ooi.occi.core import collection
from ooi.tests.tests_networks import fakes
from ooi.tests.tests_networks.middleware import test_middleware
from ooi import utils


def build_occi_network(network):
    name = network["name"]
    network_id = network["id"]
    subnet_info = network["subnet_info"]
    status = network["status"].upper()
    if status in ("ACTIVE",):
        status = "active"
    else:
        status = "inactive"

    app_url = fakes.application_url
    cats = []
    cats.append('network; '
                'scheme='
                '"http://schemas.ogf.org/occi/infrastructure#";'
                ' class="kind"; title="network resource";'
                ' rel='
                '"http://schemas.ogf.org/occi/core#resource";'
                ' location="%s/network/"' % app_url)
    cats.append('osnetwork; '
                'scheme='
                '"http://schemas.openstack.org/infrastructure/network#";'
                ' class="mixin"; title="openstack network"')
    cats.append('ipnetwork; '
                'scheme='
                '"http://schemas.openstack.org/infrastructure/network#";'
                ' class="mixin"; title="IP Networking Mixin"')

    links = []
    links.append('<%s/network/%s?action=up>; '
                 'rel="http://schemas.ogf.org/occi/'
                 'infrastructure/network/action#up"' %
                 (fakes.application_url, network_id))
    links.append('<%s/network/%s?action=down>; '
                 'rel="http://schemas.ogf.org/occi/'
                 'infrastructure/network/action#down"' %
                 (fakes.application_url, network_id))

    attrs = [
        'occi.core.id="%s"' % network_id,
        'occi.core.title="%s"' % name,
        'occi.network.state="%s"' % status,
        'org.openstack.network.ip_version="%s"' % subnet_info["ip_version"],
        'org.openstack.network.public="false"',
        'org.openstack.network.shared="false"',
        'occi.network.address="%s"' % subnet_info["cidr"],
        'occi.network.gateway="%s"' % subnet_info["gateway_ip"],
        ]
    result = []
    for c in cats:
        result.append(("Category", c))
    for a in attrs:
        result.append(("X-OCCI-Attribute", a))
    for l in links:
        result.append(("Link", l))
    return result


def create_occi_results(data):
    return network.Controller(None)._get_network_resources(data)


class TestNetworkController(test_middleware.TestMiddleware):
    """Test OCCI compute controller."""

    def setUp(self):
        super(TestNetworkController, self).setUp()

    def assertExpectedResult(self, expected, result):
        expected = ["%s: %s" % e for e in expected]
        # NOTE(aloga): the order of the result does not matter
        results = str(result.text).splitlines()
        self.assertItemsEqual(expected, results)

    @mock.patch.object(network.Controller, "index")
    def test_list_networks_empty(self, m):
        tenant = fakes.tenants["bar"]
        headers = {
            'Category': 'network; scheme="http://schema#";class="kind";',
            'X_OCCI_Attribute': 'project=%s' % tenant["id"],
        }
        url = "/network"
        req = self._build_req(url, method="GET",
                              headers=headers, content_type="text/occi")
        m.return_value = collection.Collection(
            create_occi_results(fakes.networks[tenant['id']]))
        resp = req.get_response(self.app)
        self.assertEqual(204, resp.status_code)
        expected_result = ""
        self.assertExpectedResult(expected_result, resp)
        self.assertDefaults(resp)

    @mock.patch.object(network.Controller, "index")
    def test_list_networks(self, m):
        tenant = fakes.tenants["foo"]
        m.return_value = collection.Collection(
            create_occi_results(fakes.networks[tenant['id']]))
        req = self._build_req("/network", method="GET")
        resp = req.get_response(self.app)

        self.assertEqual(200, resp.status_code)
        expected = []
        for s in fakes.networks[tenant["id"]]:
            expected.append(
                ("X-OCCI-Location",
                 utils.join_url(self.application_url + "/",
                                "network/%s" % s["id"]))
            )
        self.assertDefaults(resp)
        self.assertExpectedResult(expected, resp)

    @mock.patch.object(network.Controller, "create")
    def test_create(self, m):
        tenant = fakes.tenants["foo"]
        headers = {
            'Category': 'network; scheme="http://schema#";class="kind",' +
                        'mixinID;'
                        'scheme="http://schemas.openstack.org/template/os#";'
                        ' class=mixin',
            'X_Occi_Attribute': 'project=%s' % tenant["id"],
        }
        req = self._build_req("/network", method="POST", headers=headers)
        m.return_value = create_occi_results(fakes.networks[tenant['id']])
        resp = req.get_response(self.app)
        self.assertEqual(200, resp.status_code)

    @mock.patch.object(network.Controller, "show")
    def test_show_networks(self, m):
        tenant = fakes.tenants["foo"]

        for n in fakes.networks[tenant["id"]]:
            m.return_value = create_occi_results([n])[0]
            req = self._build_req("/network/%s" % n["id"],
                                  method="GET")
            resp = req.get_response(self.app)
            expected = build_occi_network(n)
            self.assertEqual(200, resp.status_code)
            self.assertDefaults(resp)
            self.assertExpectedResult(expected, resp)

    @mock.patch.object(network.Controller, "delete")
    def test_delete_networks(self, m):
        tenant = fakes.tenants["foo"]
        for n in fakes.networks[tenant["id"]]:
            m.return_value = create_occi_results([])
            req = self._build_req("/network/%s" % n["id"],
                                  method="DELETE")
            resp = req.get_response(self.app)
            self.assertEqual(204, resp.status_code)
            self.assertDefaults(resp)
