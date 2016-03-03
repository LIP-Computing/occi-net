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

from ooi.tests.tests_networks.integration import TestIntegration

from ooi.tests.tests_networks.integration.keystone.session import KeySession
from ooi.wsgi import OCCIMiddleware


class TestMiddleware(TestIntegration):
    def setUp(self):
        super(TestMiddleware, self).setUp()
        self.app = OCCIMiddleware(None, neutron_endpoint="http://127.0.0.1:9696/v2.0")

    def test_index(self):
        headers = {
            #'Category': 'network; scheme="http://schema#";class="kind";',
            "X_PROJECT_ID": self.project_id,
        }
        req = KeySession().create_request(self.session, headers=headers, path="/networks")
        result = req.get_response(self.app)
        self.assertEqual(200, result.status_code)
        self.assertIsNot("", result.text)

    def test_show(self):
        req = KeySession().create_request(self.session, path="/networks/%s" % self.public_network, method="GET")
        result = req.get_response(self.app)
        self.assertEqual(200, result.status_code)
        self.assertIsNot("", result.text)

    def test_create_delete_network(self):
        headers = {
            #'Category': 'network; scheme="http://schema#";class="kind";',
            "X_OCCI_Attribute": 'occi.core.title= pruebas, occi.network.ip_version=4, occi.networkinterface.address="10.1.0.1/10"',
            "X_PROJECT_ID": self.project_id,
        }
        req = KeySession().create_request(self.session, path="/networks", headers=headers, method="POST")
        result = req.get_response(self.app)
        self.assertEqual(200, result.status_code)

        net_id = result.text.split('\n')[5].split('=')[1].replace('"', '').strip()
        headers_delete = {
             "X_OCCI_Attribute": 'occi.core.id=%s' % net_id,
        }
        req = KeySession().create_request(self.session, path="/networks/%s" % net_id, headers=headers_delete, method="DELETE")
        result = req.get_response(self.app)
        self.assertEqual(204, result.status_code)

    def test_run_up_network(self):
        req = KeySession().create_request(self.session, path="/networks/%s?action=up" % self.public_network, method="POST")
        result = req.get_response(self.app)
        self.assertEqual(404, result.status_code)