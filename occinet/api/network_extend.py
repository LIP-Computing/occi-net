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

import webob.exc

import ooi.api.base
import ooi.api.helpers
from ooi.occi import validator as occi_validator
from ooi.occi.core import collection
from ooi.occi.infrastructure import compute
from ooi.occi.infrastructure import network
from ooi.occi.infrastructure import storage
from ooi.occi.infrastructure import storage_link
from ooi.openstack import contextualization
from ooi.openstack import helpers
from ooi.openstack import templates


class Controller(ooi.api.base.Controller):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.net_actions = network.NetworkResource.actions
        self.os_helper = ooi.api.helpers.OpenStackHelper(
            self.app,
            self.openstack_version
        )
