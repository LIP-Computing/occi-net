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

import uuid

from occinet.tests import fakes
from occinet.tests.middleware import test_middleware
from ooi import utils

def build_occi_network(network):
    name = network["name"]
    network_id = network["id"]
    subnet_id = fakes.subnets[network["subnets"]["id"]]["id"]
    subnet_name = fakes.subnets[network["subnets"]["id"]]["name"]


    status = network["status"].upper()
    if status in ("ACTIVE",):
        status = "active"
    else:
        status = "inactive"

    app_url = fakes.application_url
    cats = []
    cats.append('network; '
                'scheme="http://schemas.ogf.org/occi/infrastructure#"; '
                'class="kind"; title="network resource"; '
                'rel="http://schemas.ogf.org/occi/core#resource"; '
                'location="%s/network/"' % app_url)
    cats.append('%s; '
                'scheme="http://schemas.openstack.org/template/resource#"; '
                'class="mixin"; title="Subnet: %s"; '
                'rel="http://schemas.ogf.org/occi/infrastructure#resource_tpl"'
                '; '
                'location="%s/resource_tpl/%s"'
                % (subnet_id, subnet_name, app_url, subnet_id)),

    attrs = [
        'occi.core.title="%s"' % name,
        'occi.network.state="%s"' % status,
    ]



    result = []
    for c in cats:
        result.append(("Category", c))
    for a in attrs:
        result.append(("X-OCCI-Attribute", a))
    return result


class TestNetworkController(test_middleware.TestMiddleware):
    """Test OCCI compute controller."""

    def assertExpectedResult(self, expected, result):
        expected = ["%s: %s" % e for e in expected]
        # NOTE(aloga): the order of the result does not matter
        results = str(result.text).splitlines()
        self.assertItemsEqual(expected, results)

    def test_list_networks_empty(self):
        tenant = fakes.tenants["bar"]
        app = self.get_app()

        for url in ("/networks", "/networks?tenant_id=33"): #delete the parameters to check it
            req = self._build_req(url, tenant["id"], method="GET")

            req.environ["HTTP_X_PROJECT_ID"] = tenant["id"]
            # OCCIMiddleware contain a mapper independent from fake.
            # It maps only the occi components. CONTROLADOR CARGADO ES DE OOOI
            resp = req.get_response(app)

            expected_result = ""
            self.assertDefaults(resp)
            self.assertExpectedResult(expected_result, resp)
            self.assertEqual(204, resp.status_code)

    def test_list_networks(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()
        headers = {
            'X-OCCI-Attribute': 'tenant_id=%s, network_id=1' %tenant["id"],
        }

        #for url in (, "/networks/"): #todo(jorgesece): Create test with different headers
        req = self._build_req("/networks", tenant["id"], method="GET",headers=headers)
        resp = req.get_response(app)

        self.assertEqual(200, resp.status_code)
        expected = []
        for s in fakes.networks[tenant["id"]]:
            expected.append(
                ("X-OCCI-Location",
                 utils.join_url(self.application_url + "/",
                               "networkextend/%s" % s["id"]))
                )
        self.assertDefaults(resp)
        self.assertExpectedResult(expected, resp)

    def test_show_networks(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()

        for network in fakes.networks[tenant["id"]]:
            req = self._build_req("/networks/%s" % network["id"],
                                  tenant["id"], method="GET")

            resp = req.get_response(app)
            expected = build_occi_network(network)
            self.assertDefaults(resp)
            self.assertExpectedResult(expected, resp)
            self.assertEqual(200, resp.status_code)

    def test_net_not_found(self):
        tenant = fakes.tenants["foo"]

        app = self.get_app()
        req = self._build_req("/networks/%s" % uuid.uuid4().hex,
                              tenant["id"], method="GET")
        resp = req.get_response(app)
        self.assertEqual(404, resp.status_code)

    def test_action_net(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()

        for action in ("stop", "start"):
            headers = {
                'Category': (
                    '%s;'
                    'scheme="http://schemas.ogf.org/occi/infrastructure/'
                    'networks/action#";'
                    'class="action"' % action)
            }
            for network in fakes.networks[tenant["id"]]:
                req = self._build_req("/networks/%s?action=%s" % (network["id"],
                                                                 action),
                                      tenant["id"], method="POST",
                                      headers=headers)
                resp = req.get_response(app)
                self.assertDefaults(resp)
                self.assertEqual(204, resp.status_code)

    def test_invalid_action(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()

        action = "foo"
        for network in fakes.networks[tenant["id"]]:
            req = self._build_req("/networks/%s?action=%s" % (network["id"],
                                                             action),
                                  tenant["id"], method="POST")
            resp = req.get_response(app)
            self.assertDefaults(resp)
            self.assertEqual(400, resp.status_code)
"""
    def test_action_body_mismatch(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()

        action = "stop"
        headers = {
            'Category': (
                'start;'
                'scheme="http://schemas.ogf.org/occi/infrastructure/'
                'compute/action#";'
                'class="action"')
        }
        for server in fakes.servers[tenant["id"]]:
            req = self._build_req("/compute/%s?action=%s" % (server["id"],
                                                             action),
                                  tenant["id"], method="POST",
                                  headers=headers)
            resp = req.get_response(app)
            self.assertDefaults(resp)
            self.assertEqual(400, resp.status_code)

    def test_create_vm(self):
        tenant = fakes.tenants["foo"]

        app = self.get_app()
        headers = {
            'Category': (
                'compute;'
                'scheme="http://schemas.ogf.org/occi/infrastructure#";'
                'class="kind",'
                'foo;'
                'scheme="http://schemas.openstack.org/template/resource#";'
                'class="mixin",'
                'bar;'
                'scheme="http://schemas.openstack.org/template/os#";'
                'class="mixin"')
        }
        req = self._build_req("/compute", tenant["id"], method="POST",
                              headers=headers)
        resp = req.get_response(app)

        expected = [("X-OCCI-Location",
                     utils.join_url(self.application_url + "/",
                                    "compute/%s" % "foo"))]
        self.assertEqual(200, resp.status_code)
        self.assertExpectedResult(expected, resp)
        self.assertDefaults(resp)

    def test_create_vm_incomplete(self):
        tenant = fakes.tenants["foo"]

        app = self.get_app()
        headers = {
            'Category': (
                'compute;'
                'scheme="http://schemas.ogf.org/occi/infrastructure#";'
                'class="kind",'
                'bar;'
                'scheme="http://schemas.openstack.org/template/os#";'
                'class="mixin"')
        }

        req = self._build_req("/compute", tenant["id"], method="POST",
                              headers=headers)
        resp = req.get_response(app)

        self.assertEqual(400, resp.status_code)
        self.assertDefaults(resp)

    def test_create_with_context(self):
        tenant = fakes.tenants["foo"]

        app = self.get_app()
        headers = {
            'Category': (
                'compute;'
                'scheme="http://schemas.ogf.org/occi/infrastructure#";'
                'class="kind",'
                'foo;'
                'scheme="http://schemas.openstack.org/template/resource#";'
                'class="mixin",'
                'bar;'
                'scheme="http://schemas.openstack.org/template/os#";'
                'class="mixin",'
                'user_data;'
                'scheme="http://schemas.openstack.org/compute/instance#";'
                'class="mixin"'
            ),
            'X-OCCI-Attribute': (
                'org.openstack.compute.user_data="foo"'
            )
        }

        req = self._build_req("/compute", tenant["id"], method="POST",
                              headers=headers)
        resp = req.get_response(app)

        expected = [("X-OCCI-Location",
                     utils.join_url(self.application_url + "/",
                                    "compute/%s" % "foo"))]
        self.assertEqual(200, resp.status_code)
        self.assertExpectedResult(expected, resp)
        self.assertDefaults(resp)

    def test_vm_links(self):
        tenant = fakes.tenants["baz"]

        app = self.get_app()

        for server in fakes.servers[tenant["id"]]:
            req = self._build_req("/compute/%s" % server["id"],
                                  tenant["id"], method="GET")

            resp = req.get_response(app)

            self.assertDefaults(resp)
            self.assertContentType(resp)
            self.assertEqual(200, resp.status_code)

            source = utils.join_url(self.application_url + "/",
                                    "compute/%s" % server["id"])
            # volumes
            vols = server.get("os-extended-volumes:volumes_attached", [])
            for v in vols:
                vol_id = v["id"]
                link_id = '_'.join([server["id"], vol_id])

                target = utils.join_url(self.application_url + "/",
                                        "storage/%s" % vol_id)
                self.assertResultIncludesLink(link_id, source, target, resp)

            # network
            addresses = server.get("addresses", {})
            for addr_set in addresses.values():
                for addr in addr_set:
                    ip = addr["addr"]
                    link_id = '_'.join([server["id"], ip])
                    if addr["OS-EXT-IPS:type"] == "fixed":
                        net_id = "fixed"
                    else:
                        net_id = "floating"
                    target = utils.join_url(self.application_url + "/",
                                            "network/%s" % net_id)
                    self.assertResultIncludesLink(link_id, source, target,
                                                  resp)

    def test_delete_vm(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()

        for s in fakes.servers[tenant["id"]]:
            req = self._build_req("/compute/%s" % s["id"],
                                  tenant["id"], method="DELETE")
            resp = req.get_response(app)
            self.assertContentType(resp)
            self.assertEqual(204, resp.status_code)

    # TODO(enolfc): find a way to be sure that all servers
    #               are in fact deleted.
    def test_delete_all_vms(self):
        tenant = fakes.tenants["foo"]
        app = self.get_app()

        req = self._build_req("/compute/", tenant["id"], method="DELETE")
        resp = req.get_response(app)
        self.assertContentType(resp)
        self.assertEqual(204, resp.status_code)

"""

