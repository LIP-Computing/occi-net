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

import mock
import six
import webob
import webob.exc

from keystonemiddleware import auth_token
from keystone.session import KeySession

from occinet.api import network
from ooi import exception
from ooi.occi.core import collection
from ooi.occi.infrastructure import network as occi_network
from ooi.openstack import contextualization
from ooi.openstack import templates
from ooi.tests import base
from ooi.wsgi import OCCIMiddleware

from occinet.drivers.openstack import openstack_driver
from occinet.tests import fakes





class TestNetworkController(base.TestController):
    def setUp(self):
        super(TestNetworkController, self).setUp()
        self.controller = network.Controller(mock.MagicMock(), None)

    @mock.patch.object(openstack_driver.OpenStackNet, "index")
    def test_index(self, m_index):
        test_networks = [
            [],
            fakes.networks[fakes.tenants["foo"]["id"]]
        ]

        for nets in test_networks:
            m_index.return_value = nets
            result = self.controller.index(None)
            expected = self.controller._get_network_resources(nets)
            self.assertEqual(expected, result.resources)
            m_index.assert_called_with(None)

    def test_list(self):


      #  app = auth_token.AuthProtocol(app,{})
        #app.process_request() _AuthTokenRequest(req)
        #om = OCCIMiddleware(app)
        #om.process_request(req)
        key_session = KeySession()
        req = key_session.create_request_conection("dev", "passwd", "6271876e5bea4935a98cf10840f8dcb6")
        net = network.Controller(None, "/v2.0")
        lista = net.index(req)
        expected = collection.Collection
        self.assertIs(expected, lista)