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
from ooi.tests.tests_networks.keystone.session import KeySession


class TestIntegration(base.TestController):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.project_id = "fc0dd0a3c65f4c7c90d3e6dae2aa5a85"
        self.public_network = "160300ca-36a6-4448-b1b1-1728f588b87f"
        self.new_network_name = "networkOCCINET"
        self.session = KeySession().create_keystone("admin", "stack1", self.project_id)