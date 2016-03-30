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
from ooi.occi.infrastructure import network_link
from ooi.occi.infrastructure import network
from ooi.openstack import helpers


class OSFloatingIPPool(mixin.Mixin):
    scheme = helpers.build_scheme("network/floatingippool")

    def __init__(self, pool=None):
        super(OSFloatingIPPool, self).__init__(self.scheme, pool, pool)


class OSNetworkInterface(network_link.NetworkInterface):
    attributes = attr.AttributeCollection(["occi.networkinterface.address",
                                           "occi.networkinterface.gateway",
                                           "occi.networkinterface.allocation"])

    def __init__(self, source, target, mac, address, ip_id=None, pool=None):
        link_id = '_'.join([source.id, address])
        mixins = [network_link.ip_network_interface]
        if pool:
            mixins.append(OSFloatingIPPool(pool))
        super(OSNetworkInterface, self).__init__(mixins, source, target,
                                                 link_id, "eth0", mac,
                                                 "active")
        self.ip_id = ip_id
        self.attributes["occi.networkinterface.address"] = (
            attr.MutableAttribute("occi.networkinterface.address", address))
        self.attributes["occi.networkinterface.gateway"] = (
            attr.MutableAttribute("occi.networkinterface.gateway", None))
        self.attributes["occi.networkinterface.allocation"] = (
            attr.MutableAttribute("occi.networkinterface.allocation",
                                  "dynamic"))

    @property
    def address(self):
        return self.attributes["occi.networkinterface.address"].value

    @address.setter
    def address(self, value):
        self.attributes["occi.networkinterface.address"].value = value

    @property
    def gateway(self):
        return self.attributes["occi.networkinterface.gateway"].value

    @gateway.setter
    def gateway(self, value):
        self.attributes["occi.networkinterface.gateway"].value = value

    @property
    def allocation(self):
        return self.attributes["occi.networkinterface.allocation"].value

    @allocation.setter
    def allocation(self, value):
        self.attributes["occi.networkinterface.allocation"].value = value


class OSNetwork(mixin.Mixin):
    scheme = helpers.build_scheme("infrastructure/network")

    def __init__(self, ip_version, shared=False, public=False):
        attrs = [
            attr.InmutableAttribute("org.openstack.network.shared", shared),
            attr.InmutableAttribute("org.openstack.network.public", public),
            attr.InmutableAttribute("org.openstack.network.ip_version", ip_version)
        ]
        attrs = attr.AttributeCollection({a.name: a for a in attrs})

        scheme = helpers.build_scheme("infrastructure/network")
        term = "osnetwork"
        title = "openstack network"

        super(OSNetwork, self).__init__(
            scheme=scheme,
            term=term,
            title=title,
            attributes=attrs
            )

    @property
    def shared(self):
        return self.attributes["org.openstack.network.shared"].value

    @property
    def shared(self):
        return self.attributes["org.openstack.network.public"].value

    @property
    def ip_version(self):
        return self.attributes["org.openstack.network.ip_version"].value



class OSIPNetwork(mixin.Mixin):

    def __init__(self, address, gateway, allocation=None):
        attrs = [
            attr.InmutableAttribute("occi.network.address", address),
            attr.InmutableAttribute("occi.network.gateway", gateway),
            attr.InmutableAttribute("occi.network.allocation", allocation),
        ]
        attrs = attr.AttributeCollection({a.name: a for a in attrs})

        scheme = helpers.build_scheme("infrastructure/network")
        term = "osnetwork"
        title = "openstack network"

        super(OSIPNetwork, self).__init__(
            scheme=helpers.build_scheme("infrastructure/network"),
            term="ipnetwork", title="IP Networking Mixin",
            attributes=attrs)

    @property
    def address(self):
        return self.attributes["oocci.network.network.address"].value

    @property
    def gateway(self):
        return self.attributes["oocci.network.network.gateway"].value

    @property
    def allocation(self):
        return self.attributes["occi.network.network.allocation"].value