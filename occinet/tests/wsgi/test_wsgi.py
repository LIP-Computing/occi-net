# -*- coding: utf-8 -*-

# Copyright 2015 LIP
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
from occinet import wsgi
from occinet.wsgi.middleware import OCCINetworkMiddleware



@webob.dec.wsgify
def fake_app(req):
    resp = webob.Response("Foo")
    return resp


class FakeController(object):
    def index(self, *args, **kwargs):
        return None

    def create(self, req, body):
        raise webob.exc.HTTPNotImplemented()

    def delete(self, req, id):
        raise webob.exc.HTTPNotImplemented()

    def show(self, req, id):
        # Returning a ResponseObject should stop the pipepline
        # so the application won't be called.
        resp = wsgi.ResponseObject([])
        return resp


class FakeMiddleware(OCCINetworkMiddleware):
    def _setup_routes(self):
        self.resources["foo"] = wsgi.ResourceNet(FakeController())
        self.mapper.resource("foo", "foos",
                             controller=self.resources["foo"])


class TestMiddleware(base.TestCase):
    def setUp(self):
        super(TestMiddleware, self).setUp()

        self.app = FakeMiddleware(fake_app)

    def test_index(self):
        result = webob.Request.blank("/foos",
                                     method="GET").get_response(self.app)
        self.assertEqual(200, result.status_code)
        self.assertEqual("", result.text)

    def test_show(self):
        result = webob.Request.blank("/foos/id890234",
                                     method="GET").get_response(self.app)
        self.assertEqual(204, result.status_code)
        self.assertEqual("", result.text)
