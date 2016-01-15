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

from ooi.occi.core import attribute as attr
from ooi.occi.core import kind
from ooi.occi.infrastructure.network import NetworkResource
from ooi.occi import helpers


class Network(NetworkResource):
    attributes = attr.AttributeCollection(["occinet.network.shared",
                                           "occinet.network.adminstate",
                                           "occinet.network.tenantid",
                                           "occinet.subnetwork.name",
                                           "occinet.subnetwork.ip_version",
                                           "occinet.subnetwork.pool_start",
                                           "occinet.subnetwork.pool_end",
                                           ])
    scheme = helpers.build_scheme("infrastructure/network",)
    term = "networks"

    kind = kind.Kind(scheme, term, 'network extended', attributes=attributes,
                     location='networks/',  related=[NetworkResource.kind])

    def __init__(self, title=None, summary=None, id=None,vlan=None, label=None, state=None,
                 shared=None, adminstate=None, tenantid=None, subnet_name=None, ip_start=None
                 , ip_end=None, ip_version=None):
        super(Network, self).__init__(title=title, summary=summary, id=id, vlan=vlan,
                                      label=label, state=state)
        self.attributes["occinet.network.shared"] = attr.MutableAttribute(
            "occinet.network.shared", shared)
        self.attributes["occinet.network.adminstate"] = attr.MutableAttribute(
            "occinet.network.adminstate", adminstate)
        self.attributes["occinet.network.tenantid"] = attr.MutableAttribute(
            "occinet.network.tenantid", tenantid)
        #subnet
        self.attributes["occinet.subnetwork.name"] = attr.MutableAttribute(
            "occinet.subnetwork.name", subnet_name)
        self.attributes["occinet.subnetwork.ip_version"] = attr.InmutableAttribute(
            "occinet.network.ip_version", ip_version)
        self.attributes["occinet.subnetwork.pool_start"] = attr.InmutableAttribute(
            "occinet.subnetwork.pool_start", ip_start)
        self.attributes["occinet.subnetwork.pool_end"] = attr.InmutableAttribute(
            "occinet.subnetwork.pool_end", ip_end)

    @property
    def shared(self):
        return self.attributes["occinet.network.shared"].value

    @shared.setter
    def shared(self, value):
        self.attributes["occinet.network.shared"].value = value

    @property
    def adminstate(self):
        return self.attributes["occinet.network.adminstate"].value

    @adminstate.setter
    def adminstate(self, value):
        self.attributes["occinet.network.adminstate"].value = value

    @property
    def tenantid(self):
        return self.attributes["occinet.network.tenantid"].value
    # SUBRED
    @property
    def subnet_name(self):
        return self.attributes["occinet.subnetwork.name"].value

    @subnet_name.setter
    def subnet_name(self, value):
        self.attributes["occinet.subnetwork.name"].value = value

    @property
    def ip_version(self):
        return self.attributes["occinet.subnetwork.ip_version"].value

    @property
    def ip_start(self):
        return self.attributes["occinet.subnetwork.ip_start"].value

    @property
    def ip_end(self):
        return self.attributes["occinet.subnetwork.ip_end"].value