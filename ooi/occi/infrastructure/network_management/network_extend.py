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
from ooi.occi.core import mixin
from ooi.occi import helpers
from ooi.occi.infrastructure import network



class Network(network.NetworkResource):
    attributes = attr.AttributeCollection(["org.openstack.network.shared",
                                           "org.openstack.network.tenantid",
                                           "org.openstack.network.ip_version"
                                           ])
    scheme = helpers.build_scheme("infrastructure/network",)
    term = "management"
    kind = kind.Kind(scheme, term, 'network management', attributes=attributes,
                     location='networkmanagement/',
                     related=[network.NetworkResource.kind])

    def __init__(self, title=None, summary=None,
                 id=None, vlan=None, label=None, state=None,
                 shared=None, tenantid=None,
                 ip_version=None, mixins=[]):

        super(Network, self).__init__(title=title,
                                      summary=summary, id=id, vlan=vlan,
                                      label=label, state=state, mixins=mixins)
        self.attributes["org.openstack.network.shared"] = attr.MutableAttribute(
            "org.openstack.network.shared", shared)
        self.attributes["org.openstack.network.tenantid"] = attr.MutableAttribute(
            "org.openstack.network.tenantid", tenantid)
        # # subnet
        self.attributes["org.openstack.network.ip_version"] = (
            attr.InmutableAttribute(
                "org.openstack.network.ip_version", ip_version))
        # self.attributes["occi.network.address"] = (
        #     attr.InmutableAttribute(
        #         "occi.network.address", address))
        # self.attributes["occi.network.gateway"] = (
        #     attr.InmutableAttribute(
        #         "occi.network.gateway", gateway))


    @property
    def shared(self):
        return self.attributes["org.openstack.network.shared"].value

    @shared.setter
    def shared(self, value):
        self.attributes["org.openstack.network.shared"].value = value

    @property
    def tenantid(self):
        return self.attributes["org.openstack.network.tenantid"].value

    # SUBRED
    @property
    def ip_version(self):
        return self.attributes["org.openstack.network.ip_version"].value

    # @property
    # def address(self):
    #     return self.attributes["occi.network.address"].value
    #
    # @property
    # def gateway(self):
    #     return self.attributes["occi.network.gateway"].value


class NetworkIP(mixin.Mixin):

    def __init__(self, address, gateway, allocation=None):

        scheme = helpers.build_scheme('infrastructure/networkmanagement',)
        attrs = network.ip_network.attributes
        title = "IP network management"
        super(NetworkIP, self).__init__(
            scheme=scheme, title=title, term="ip_network_manage",
            related=[network.ip_network],
            attributes=attrs)
        self.attributes["occi.network.address"] = attr.MutableAttribute(
            "occi.network.address", address)
        self.attributes["occi.network.gateway"] = attr.MutableAttribute(
            "occi.network.gateway", gateway)
        self.attributes["cci.network.allocation"] = attr.MutableAttribute(
            "cci.network.allocation", allocation)

    @property
    def address(self):
        return self.attributes["occi.network.address"].value

    @address.setter
    def address(self, value):
        self.attributes["occi.network.address"].value = value

    @property
    def gateway(self):
        return self.attributes["occi.network.gateway"].value

    @gateway.setter
    def gateway(self, value):
        self.attributes["occi.network.gateway"].value = value

    @property
    def allocation(self):
        return self.attributes["occi.network.allocation"].value

    @allocation.setter
    def allocation(self, value):
        self.attributes["occi.network.allocation"].value = value
        "occi.network.allocation"