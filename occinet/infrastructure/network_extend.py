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
from ooi.occi.core import mixin
from ooi.occi.core import kind
from ooi.occi.infrastructure.network import NetworkResource
from ooi.occi import helpers


class Network(NetworkResource):
    attributes = attr.AttributeCollection(["occinet.network.shared",
                                           "occinet.network.adminstate",
                                           "occinet.network.tenantid",
                                           "occinet.network.subnets"])
    scheme = helpers.build_scheme("infrastructure/network",)
    term = "networks"

    kind = kind.Kind(scheme, term, 'network extended', attributes=attributes,
                     location='networks/',  related=[NetworkResource.kind])

    def __init__(self, title=None, summary=None, id=None,vlan=None, label=None, state=None,
                 shared=None, adminstate=None, tenantid=None, subnets=[]):
        super(Network, self).__init__(title=title, summary=summary, id=id, vlan=vlan,
                                      label=label, state=state, mixins=subnets)
        self.attributes["occinet.network.shared"] = attr.MutableAttribute(
            "occinet.network.shared", shared)
        self.attributes["occinet.network.adminstate"] = attr.MutableAttribute(
            "occinet.network.adminstate", adminstate)
        self.attributes["occinet.network.tenantid"] = attr.MutableAttribute(
            "occinet.network.tenantid", tenantid)
        self.attributes["occinet.network.tenantid"] = attr.MutableAttribute(
            "occinet.network.tenantid", tenantid)
        self.attributes["occinet.network.subnets"] = attr.MutableAttribute(
            "occinet.network.subnets", None) #todo(jorgesece): subnets should be and Mixin class.


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

    @tenantid.setter
    def tenantid(self, value):
        self.attributes["occinet.network.tenantid"].value = value

    @property
    def subnets(self):
        return self.attributes["occinet.network.subnets"].value

    @subnets.setter
    def subnets(self, value):
        self.attributes["occinet.network.subnets"].value.append(value)




#
#WE DO NOT USE THIS CLASS, IT WAS JUST TO TEST THE
#
class NetworkMixin(mixin.Mixin):
    attributes = attr.AttributeCollection(["occinet.network.shared",
                                           "occinet.network.adminstate",
                                           "occinet.network.tenantid"])
    scheme = helpers.build_scheme("infrastructure/network",)
    term = "networkExtend"

    def __init__(self, title=None, summary=None, id=None,vlan=None, label=None, state=None, shared=None, adminstate=None, tenantid=None):

        super(Network, self).__init__(self.scheme, self.term, title, attributes=self.attributes)
        self.attributes["occinet.network.shared"] = attr.MutableAttribute(
            "occinet.network.shared", shared)
        self.attributes["occinet.network.adminstate"] = attr.MutableAttribute(
            "occinet.network.adminstate", adminstate)
        self.attributes["occinet.network.tenantid"] = attr.MutableAttribute(
            "occinet.network.tenantid", tenantid)
        self.network = NetworkResource(title, summary, id, vlan, label, state)

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

    @tenantid.setter
    def tenantid(self, value):
        self.attributes["occinet.network.tenantid"].value = value

    def networkResource(self):
        return self.network

