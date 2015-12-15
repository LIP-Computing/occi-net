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

import webob

from ooi.api import base
from occinet.drivers.openstack.openstack_driver import OpenStackNet  # it was import ooi.api.helpers
from ooi import exception
from ooi.occi.core import collection


from occinet.infrastructure.network_extend import Network
#from occinet.drivers.openstack import templates

FLOATING_PREFIX = "floating"
FIXED_PREFIX = "fixed"


def _build_network(name, prefix=None):
    if prefix:
        network_id = '/'.join([prefix, name])
    else:
        network_id = name
    return Network(title=name, id=network_id, state="active")


class Controller(base.Controller):
    def __init__(self, *args, **kwargs):
        super(Controller, self).__init__(*args, **kwargs)
        self.os_helper = OpenStackNet(
            self.app,
            self.openstack_version
        )

    def _get_network_resources(self, networks):
        occi_network_resources = []
        if networks:
            for s in networks:
                s = Network(title=s["name"], id=s["id"])
                occi_network_resources.append(s)

        return occi_network_resources

    def index(self, req, parameters=None):

        occi_networks = self.os_helper.index(req, parameters)
        occi_network_resources = self._get_network_resources(occi_networks)

        return collection.Collection(resources=occi_network_resources)

    def show(self, req, id, parameters=None):
        # get info from server
        resp = self.os_helper.get_network(req, id, parameters)
        state =resp["status"]
        # get info from subnet #TODO(jorgesece): we have to define subnets infrastructuer (mixing or resource?)
        subnets_array = []
        for subnet_id in resp["subnets"]:
            subnets_array.append(subnet_id)
            #subnet = self.os_helper.get_subnets(req, subnet_id)
            #subnets_array.append(subnet)

   #     os_tpl = templates.OpenStackOSTemplate(image["id"],     image["name"])

        # build the network object
        net = Network(title=resp["name"], id=resp["id"],state=state, subnets=subnets_array)

        return net

