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


from ooi.tests.tests_networks.integration import  TestIntegration

from ooi import exception
from ooi.wsgi import Request
from ooi.api import network_link as link_controller
from ooi.occi.infrastructure import network_link
from ooi.tests.tests_networks.integration.keystone.session import KeySession
from ooi.tests import fakes_neutron as fakes


class TestIntegrationNetworkLink(TestIntegration):

    def setUp(self):
        super(TestIntegrationNetworkLink, self).setUp()
        self.req = Request(KeySession().create_request_nova(self.session, path="/",
                                                            environ={},
                                                            headers={"X_PROJECT_ID": self.project_id}
                                                            ).environ)
        self.controller = link_controller.Controller(app=None,openstack_version="/v2.1")

    def test_index(self):
        occi = self.controller.index(self.req)
        self.assertIsNotNone(occi)

    def test_show(self):
        link_id = '63ec7dbc-5597-4455-925a-763b8891aa1f_'\
                  'cd48b7dd-9ac8-44fc-aec0-5ea679941ced_12.0.0.4'
        occi = self.controller.show(self.req, link_id)
        self.assertIsNotNone(occi)
        server_id, network_id, server_addr = link_id.split('_', 2)
        self.assertEquals(occi.target.id, network_id)
        self.assertEquals(occi.source.id, server_id)
        self.assertEquals(occi.address, server_addr)

    def test_create_delete_private(self):
        compute_id = '63ec7dbc-5597-4455-925a-763b8891aa1f'
        net_id = 'cd48b7dd-9ac8-44fc-aec0-5ea679941ced'
        parameters = {
                "occi.core.target": net_id,
                "occi.core.source": compute_id,
            }
        categories = {network_link.NetworkInterface.kind}

        self.req.headers = fakes.create_header_occi(parameters, categories, self.project_id)
        out = self.controller.create(self.req)
        self.assertIsNotNone(out)
        self.assertIsNotNone(out.resources)
        link_id = out.resources[0].id
        out = self.controller.delete(self.req, link_id)
        self.assertEqual([], out)

    def test_create_public(self):
        compute_id = '63ec7dbc-5597-4455-925a-763b8891aa1f'
        net_id = 'PUBLIC'
        parameters = {
                "occi.core.target": net_id,
                "occi.core.source": compute_id,
            }
        categories = {network_link.NetworkInterface.kind}

        self.req.headers = fakes.create_header_occi(parameters, categories, self.project_id)
        out = self.controller.create(self.req)
        self.assertIsNotNone(out)
        self.assertIsNotNone(out.resources)
        link_id = out.resources[0].id

        out = self.controller.delete(self.req, link_id)
        self.assertEqual([], out)

    def test_delete_private_not_found(self):
        link_id = '63ec7dbc-5597-4455-925a-763b8891aa1f_'\
                  'cd48b7dd-9ac8-44fc-aec0-5ea679941ced_12.0.0.9'
        self.assertRaises(exception.LinkNotFound, self.controller.delete, self.req, link_id)

    def test_delete_public_not_found(self):
        link_id = '63ec7dbc-5597-4455-925a-763b8891aa1f_' \
                  'PUBLIC_172.24.4.25'
        self.assertRaises(exception.LinkNotFound, self.controller.delete, self.req, link_id)





