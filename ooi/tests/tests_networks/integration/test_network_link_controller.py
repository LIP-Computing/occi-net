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
from ooi.api import network as net_controler
from ooi.occi.infrastructure import network
from ooi.tests.tests_networks.integration.keystone.session import KeySession
from ooi.tests.tests_networks import fakes



class TestIntegrationNetworkLink(TestIntegration):

    def setUp(self):
        super(TestIntegrationNetworkLink, self).setUp()
        self.req = Request(KeySession().create_request(self.session, path="/",
                                                       environ={},
                                                       headers={"X_PROJECT_ID": self.project_id}).environ)

        self.controller = net_controler.Controller("http://127.0.0.1:9696/v2.0")



    def test_create_delete_network_with_subnet(self):
        compute_id = 'bb62976a-13fe-4c23-9343-324149c63dbc'

        fip = self.controller.assign_floating_ip(self.req, compute_id)
        self.controller.release_floating_ip(self.req, compute_id)
