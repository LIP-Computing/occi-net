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
from ooi.tests.tests_networks.integration.keystone.session import KeySession


class TestIntegration(base.TestController):

    def setUp(self):
        super(TestIntegration, self).setUp()
        self.project_id = "6a7f9cdcdcc049b1b9ca849b9b678255"
        self.public_network = "cd58eade-79a1-4633-8fb7-c7d8a030c942"
        self.new_network_name = "networkOCCINET"
        self.session = KeySession().create_keystone("admin", "stack1", self.project_id)