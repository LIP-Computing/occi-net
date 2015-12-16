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

from ooi.tests import base

from  occinet.wsgi import parsers


class TestParser(base.TestCase):
    """Test OpenStack Driver against DevStack."""

    def setUp(self):
        super(TestParser, self).setUp()
       # self.driver = OpenStackNet

    def test_query_string(self): #TODO(jorgesece): the fake driver should be improved to make parametriced query tests
        query = parsers.get_query_string({"tenant_id" : "foo", "name" : "public"})

        self.assertEqual(25, query.__len__())

    def test_param_from_headers(self): #TODO(jorgesece): the fake driver should be improved to make parametriced query tests
        tenant_id="33"
        headers = {
            'HTTP_X_OCCI_ATTRIBUTE': {'tenant_id' : tenant_id, 'network_id' : 1},
        }

        #TextParse from ooi.wsgi I can use well. I will come back to it
        parameters = parsers.ParserNet(headers, None).get_attributes_from_dict()

        headers2 = {
            "HTTP_X_OCCI_ATTRIBUTE": 'tenant_id=%s, network_id=1' % tenant_id,
        }
        parameters2 = parsers.ParserNet(headers2, None).get_attributes_from_headers()

        self.assertEqual(2,parameters.__len__())
        self.assertEqual(2,parameters2.__len__())
        self.assertEqual(tenant_id, parameters2['tenant_id'])
        self.assertEqual(parameters['tenant_id'], parameters2['tenant_id'])

    def test_make_body(self):
        parameters = {"tenant_id" : "foo", "name" : "public"}
        body = parsers.ParserNet(None,None).make_body(parameters)

        self.assertIsNotNone(body["network"])
        self.assertEqual(2, body["network"].__len__())


