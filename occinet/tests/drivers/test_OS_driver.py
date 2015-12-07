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

import collections


from ooi import exception
from ooi.tests import base
from ooi.wsgi import parsers
from occinet.drivers.openstack.openstack_driver import OpenStackNet  # it was import ooi.api.helpers
from occinet.wsgi import parsers

class TestOSDriver(base.TestCase):
    """Test OpenStack Driver against DevStack."""

    def setUp(self):
        super(TestOSDriver, self).setUp()
       # self.driver = OpenStackNet

    def test_query_string(self): #TODO(jorgesece): the fake driver should be improved to make parametriced query tests
        query = parsers.get_query_string({"tenant_id" : "foo", "name" : "public"})

        self.assertEqual(25, query.__len__())


