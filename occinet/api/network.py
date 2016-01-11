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

from occinet.api.helpers import OpenStackNet  # it was import ooi.api.helpers
from occinet.infrastructure.network_extend import Network
from ooi.api import base
from ooi.occi.core import collection


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

    @staticmethod
    def _filter_attributes(parameters):
        if parameters:
            attributes = parameters.get("attributes", None)
        else:
            attributes = None
        return attributes

    @staticmethod
    def _get_network_resources(networks):
        occi_network_resources = []
        if networks:
            for s in networks:
                s = Network(title=s["name"], id=s["id"])
                occi_network_resources.append(s)

        return occi_network_resources

    def index(self, req, parameters=None):
        attributes = self._filter_attributes(parameters)
        occi_networks = self.os_helper.index(req, attributes)
        occi_network_resources = self._get_network_resources(occi_networks)

        return collection.Collection(resources=occi_network_resources)

    def show(self, req, id, parameters=None):
        # get info from server
        resp = self.os_helper.get_network(req, id)
        state = resp["status"]
        # get info from subnet
        net = Network(title=resp["name"], id=resp["id"],state=state)

        return net

    def create(self, req, parameters, body=None):
        #FIXME(jorgesece): Body is coming from OOI resource class and is not used
        attributes = self._filter_attributes(parameters)
        net = self.os_helper.create_network(req, attributes)
        occi_network_resources = self._get_network_resources([net])

        return occi_network_resources[0]

    def delete(self, req, parameters):
        attributes = self._filter_attributes(parameters)
        network_id = self.os_helper.delete_network(req, attributes)

        return []