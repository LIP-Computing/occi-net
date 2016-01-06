# Copyright 2015 LIP - Lisboa
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
from ooi.occi.core import resource
from ooi.occi.core import kind
from ooi.occi import helpers

from ooi.occi.core import mixin


class Subnetwork(mixin.Mixin): #TODO(jorgesece):create routes Mixin.

    scheme = helpers.build_scheme("infrastructure/subnetwork",)
    term = "subnetwork"
    def __init__(self, title=None, id=None, start=None, end=None, ip_version=None, cidr=None, host_routes=[]):
        _attributes = [
            attr.MutableAttribute("occinet.subnetwork.start", start),
            attr.MutableAttribute("occinet.subnetwork.end", end),
            attr.MutableAttribute("occinet.subnetwork.ip_version", ip_version),
            attr.MutableAttribute("occinet.subnetwork.cidr", cidr),
        ]

        _att = attr.AttributeCollection({a.name: a for a in _attributes})
        location = 'subnetworks/%s' % id
        super(Subnetwork, self).__init__(scheme=self.scheme, term=self.term, title=title
                                        , attributes=_att, location=location, related=host_routes)

    @property
    def start(self):
        return self.attributes["occinet.subnetwork.start"].start

    @start.setter
    def shared(self, value):
        self.attributes["occinet.subnetwork.start"].value = value

    @property
    def end(self):
        return self.attributes["occinet.subnetwork.end"].end

    @end.setter
    def end(self, value):
        self.attributes["occinet.subnetwork.end"].value = value

    @property
    def ip_version(self):
        return self.attributes["occinet.subnetwork.ip_version"].value

    @ip_version.setter
    def ip_version(self, value):
        self.attributes["occinet.subnetwork.ip_version"].value = value

    @property
    def cidr(self):
        return self.attributes["occinet.subnetwork.cidr"].value

    @cidr.setter
    def cidr(self, value):
        self.attributes["occinet.subnetwork.cidr"].value.append(value)


class SubnetworkResource(resource.Resource): #FIXME(jorgesece): this class is not used, we decided to use Mixin
    attributes = attr.AttributeCollection(["occinet.subnetwork.start",
                                           "occinet.subnetwork.end",
                                           "occinet.subnetwork.ip_version",
                                           "occinet.subnetwork.cidr",
                                           "occinet.subnetwork.host_routes" ])
    _scheme = helpers.build_scheme("infrastructure/network",)
    _term = "subnetwork"
    kind = kind.Kind(_scheme, _term, 'subnetwork', attributes=attributes, location='subnetwork/',
                     related=[resource.Resource.kind])

    def __init__(self, title=None, summary=None, id=None, start=None, end=None, ip_version=None, cidr=None, host_routes=[], mixins=[]):

        super(Subnetwork, self).__init__(title=title, summary=summary, id=id, mixins=mixins)
        self.attributes["occinet.subnetwork.start"] = attr.MutableAttribute("occinet.subnetwork.start", start)
        self.attributes["occinet.subnetwork.end"] = attr.MutableAttribute("occinet.subnetwork.end", end)
        self.attributes["occinet.subnetwork.ip_version"] = attr.MutableAttribute("occinet.subnetwork.ip_version",
                                                                                 ip_version)
        self.attributes["occinet.subnetwork.cidr"] = attr.MutableAttribute("occinet.subnetwork.cidr", cidr)
        self.attributes["occinet.subnetwork.host_routes"] = attr.MutableAttribute("occinet.subnetwork.host_routes",
                                                                                  host_routes)


    @property
    def start(self):
        return self.attributes["occinet.subnetwork.start"].start

    @start.setter
    def shared(self, value):
        self.attributes["occinet.subnetwork.start"].value = value

    @property
    def end(self):
        return self.attributes["occinet.subnetwork.end"].end

    @end.setter
    def end(self, value):
        self.attributes["occinet.subnetwork.end"].value = value

    @property
    def ip_version(self):
        return self.attributes["occinet.subnetwork.ip_version"].value

    @ip_version.setter
    def ip_version(self, value):
        self.attributes["occinet.subnetwork.ip_version"].value = value

    @property
    def cidr(self):
        return self.attributes["occinet.subnetwork.cidr"].value

    @cidr.setter
    def cidr(self, value):
        self.attributes["occinet.subnetwork.cidr"].value.append(value)

    @property
    def host_routes(self):
        return self.attributes["occinet.subnetwork.host_routes"].value

    @host_routes.setter
    def host_routes(self, value):
        self.attributes["occinet.subnetwork.host_routes"].value.append(value)
