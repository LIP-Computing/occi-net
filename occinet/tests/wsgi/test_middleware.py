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
from occinet.tests import fakes
from ooi.tests.middleware import test_middleware as testmi
from occinet.wsgi.middleware import OCCIMiddleware



class TestMiddleware(testmi.TestMiddleware):
    """OCCI middleware test without Accept header.

    According to the OCCI HTTP rendering, no Accept header
    means text/plain.
    """

    def setUp(self):
        super(TestMiddleware, self).setUp()

    def get_app(self, resp=None):
        return OCCIMiddleware(fakes.FakeApp(), openstack_version="/v2.0")