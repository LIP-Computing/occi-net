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

import webob
import webob.dec
import webob.exc

from ooi.tests import base
from occinet.wsgi.parsers import ParserNet

from occinet.wsgi.middleware import OCCINetworkMiddleware
from keystone.session import KeySession


class TestMiddleware(base.TestCase):
    def setUp(self):
        super(TestMiddleware, self).setUp()
        self.project_id = "86bf9730b23d4817b431f4c34cc9cc8e"
        self.public_network = "cd58eade-79a1-4633-8fb7-c7d8a030c942"
        self.session = KeySession().create_keystone("admin", "stack1", self.project_id)
        self.app = OCCINetworkMiddleware(None,openstack_version="/v2.0")

    def test_index(self):
        req = KeySession().create_request(self.session, path="/networks")
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
            # "X_OCCI_ATTRIBUTE": 'tenant_id=%s, name=pruebas' % (self.project_id),
            "X_OCCI_ATTRIBUTE": 'project=%s, occi.core.title=pruebas' % (self.project_id),
        }
        req = KeySession().create_request(self.session, path="/networks", headers=headers, method="POST")
        result = req.get_response(self.app)
        self.assertEqual(200, result.status_code)

        net_id = result.text.split('\n')[2].split('=')[1];
        headers_delete = {
             "X_OCCI_ATTRIBUTE": 'occi.core.id=%s' % net_id,
        }
        req = KeySession().create_request(self.session, path="/networks", headers=headers_delete, method="DELETE")
        result = req.get_response(self.app)
        self.assertEqual(204, result.status_code)

