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


class Subnetwork(resource.Resource): #FIXME(jorgesece): this class is still not used
    attributes = attr.AttributeCollection(["occinet.subnetwork.start",
                                           "occinet.subnetwork.end",
                                           "occinet.subnetwork.ip_version",
                                           "occinet.subnetwork.cidr",
                                           "occinet.subnetwork.host_routes" ])
    _scheme = helpers.build_scheme("infrastructure/network",)
    _term = "subnetwork"

    kind = kind.Kind(_scheme, _term, 'subnetwork', attributes=attributes, location='subnetwork/',
                     related=[kind.kind])

    def __init__(self, title=None, summary=None, id=None, start=None, end=None, ip_version=None, cidr=None, routes=[]):

        super(Subnetwork, self).__init__(title=title, summary=summary, id=id)
        self.attributes["occinet.subnetwork.start"] = attr.MutableAttribute("occinet.subnetwork.start", start)
        self.attributes["occinet.subnetwork.end"] = attr.MutableAttribute("occinet.subnetwork.end", end)
        self.attributes["occinet.subnetwork.ip_version"] = attr.MutableAttribute("occinet.subnetwork.ip_version",
                                                                                 ip_version)
        self.attributes["occinet.subnetwork.cidr"] = attr.MutableAttribute("occinet.subnetwork.cidr", cidr)
        self.attributes["occinet.subnetwork.host_routes"] = attr.MutableAttribute("occinet.subnetwork.host_routes",
                                                                                  routes) #todo(jorgesece):create routes.
