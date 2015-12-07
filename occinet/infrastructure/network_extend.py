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

from ooi.occi.core import attribute as attr
from ooi.occi.core import mixin
from ooi.occi.core import kind
from ooi.occi.infrastructure.network import NetworkResource
from ooi.occi import helpers


class Network(NetworkResource):
    attributes = attr.AttributeCollection(["occi.network.shared",
                                           "occi.network.adminstate",
                                           "occi.network.tenantid"])
    _scheme = helpers.build_scheme("infrastructure/network/",)
    _term = "networkextend"

    kind = kind.Kind(_scheme, _term, 'network extend', attributes, 'networkextend/')

    def __init__(self, title=None, summary=None, id=None,vlan=None, label=None, state=None, shared=None, adminstate=None, tenantid=None):

        super(Network, self).__init__(title=title, summary=summary, id=id, vlan=vlan, label=label, state=state)
        self.attributes["occi.network.shared"] = attr.MutableAttribute(
            "occi.network.shared", shared)
        self.attributes["occi.network.adminstate"] = attr.MutableAttribute(
            "occi.network.adminstate", adminstate)
        self.attributes["occi.network.tenantid"] = attr.MutableAttribute(
            "occi.network.tenantid", tenantid)


    @property
    def shared(self):
        return self.attributes["occi.network.shared"].value

    @shared.setter
    def shared(self, value):
        self.attributes["occi.network.shared"].value = value

    @property
    def adminstate(self):
        return self.attributes["occi.network.adminstate"].value

    @adminstate.setter
    def adminstate(self, value):
        self.attributes["occi.network.adminstate"].value = value

    @property
    def tenantid(self):
        return self.attributes["occi.network.tenantid"].value

    @tenantid.setter
    def tenantid(self, value):
        self.attributes["occi.network.tenantid"].value = value


class NetworkMixin(mixin.Mixin):
    attributes = attr.AttributeCollection(["occi.network.shared",
                                           "occi.network.adminstate",
                                           "occi.network.tenantid"])
    scheme = helpers.build_scheme("infrastructure/network",)
    term = "networkExtend"

    def __init__(self, title=None, summary=None, id=None,vlan=None, label=None, state=None, shared=None, adminstate=None, tenantid=None):

        super(Network, self).__init__(self.scheme, self.term, title, attributes=self.attributes)
        self.attributes["occi.network.shared"] = attr.MutableAttribute(
            "occi.network.shared", shared)
        self.attributes["occi.network.adminstate"] = attr.MutableAttribute(
            "occi.network.adminstate", adminstate)
        self.attributes["occi.network.tenantid"] = attr.MutableAttribute(
            "occi.network.tenantid", tenantid)
        self.network = NetworkResource(title, summary, id, vlan, label, state)

    @property
    def shared(self):
        return self.attributes["occi.network.shared"].value

    @shared.setter
    def shared(self, value):
        self.attributes["occi.network.shared"].value = value

    @property
    def adminstate(self):
        return self.attributes["occi.network.adminstate"].value

    @adminstate.setter
    def adminstate(self, value):
        self.attributes["occi.network.adminstate"].value = value

    @property
    def tenantid(self):
        return self.attributes["occi.network.tenantid"].value

    @tenantid.setter
    def tenantid(self, value):
        self.attributes["occi.network.tenantid"].value = value

    def networkResource(self):
        return self.network

