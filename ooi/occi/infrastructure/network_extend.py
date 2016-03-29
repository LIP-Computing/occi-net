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
from ooi.occi import helpers
from ooi.occi.infrastructure import network


class Network2(network.NetworkResource):
    attributes = attr.AttributeCollection(["org.openstack.network.shared",
                                           "org.openstack.network.tenantid",
                                           "org.openstack.network.ip_version",
                                           "occi.network.address",
                                           "occi.network.gateway",
                                           ])
    scheme = helpers.build_scheme("infrastructure/network",)
    term = "networkmanagement"
    kind = kind.Kind(scheme, term, 'network extended', attributes=attributes,
                     location="networkmanagement/",
                     related=[network.NetworkResource.kind])

    def __init__(self, title=None, summary=None,
                 id=None, vlan=None, label=None, state=None,
                 shared=None, tenantid=None,
                 address=None, gateway=None, ip_version=None):

        super(Network, self).__init__(title=title,
                                      summary=summary, id=id, vlan=vlan,
                                      label=label, state=state)
        self.attributes["org.openstack.network.shared"] = attr.MutableAttribute(
            "org.openstack.network.shared", shared)
        self.attributes["org.openstack.network.tenantid"] = attr.MutableAttribute(
            "org.openstack.network.tenantid", tenantid)
        # subnet
        self.attributes["org.openstack.network.ip_version"] = (
            attr.MutableAttribute(
                "org.openstack.network.ip_version", ip_version))
        self.attributes["occi.network.address"] = (
            attr.MutableAttribute(
                "occi.network.address", address))
        self.attributes["occi.network.gateway"] = (
            attr.MutableAttribute(
                "occi.network.gateway", gateway))


    @property
    def shared(self):
        return self.attributes["org.openstack.network.shared"].value

    @shared.setter
    def shared(self, value):
        self.attributes["org.openstack.network.shared"].value = value

    @property
    def tenantid(self):
        return self.attributes["org.openstack.network.tenantid"].value

    @property
    def tenantid(self, value):
        self.attributes["org.openstack.network.tenantid"].value = value

    # SUBRED
    @property
    def ip_version(self):
        return self.attributes["org.openstack.network.ip_version"].value

    @ip_version.setter
    def ip_version(self, value):
        self.attributes["org.openstack.network.ip_version"].value = value

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
    def gateway(self,value):
        self.attributes["occi.network.gateway"].value = value
