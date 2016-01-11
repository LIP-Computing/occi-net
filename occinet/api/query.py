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

from ooi.api import base
import ooi.api.helpers
from ooi.occi.core import entity
from ooi.occi.core import link
from ooi.occi.core import resource
from ooi.occi.infrastructure import templates as infra_templates

from occinet.infrastructure import network_extend


class Controller(base.Controller):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.os_helper = ooi.api.helpers.OpenStackHelper(
            self.app,
            self.openstack_version
        )



    def index(self, req):# todo(jorgesece): Merge it with query compute
        l = []

        # OCCI Core Kinds:
        l.append(entity.Entity.kind)
        l.append(resource.Resource.kind)
        l.append(link.Link.kind)

         # OCCI infra network
        #prueba
        l.append(infra_templates.os_tpl)
        l.append(network_extend.Network.kind)

        return l
