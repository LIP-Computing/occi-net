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

from occi.core import attribute
from occi.core import mixin
from occinet.drivers.openstack import helpers

_OPENSTACK_PATH='org.openstack'


class OpenStackUserData(mixin.Mixin):

    def __init__(self, user_data=None):
        self.scheme = helpers.build_scheme("network/instance")
        self.resource_name = "network"
        self.term = "user_data"
        attrs = [
            attribute.InmutableAttribute("%s.%s.%s" % (_OPENSTACK_PATH,self.resource_name,self.term),
                                         user_data),
        ]

        attrs = attribute.AttributeCollection({a.name: a for a in attrs})

        super(OpenStackUserData, self).__init__(
            OpenStackUserData.scheme, OpenStackUserData.term,
            "Contextualization extension - user_data",
            attributes=attrs)

    @property
    def user_data(self):
        return self.attributes["%s.%s.%s" % (_OPENSTACK_PATH,self.resource_name,self.term)].value


class OpenStackPublicKey(mixin.Mixin):

    def __init__(self, name = None, data = None):
        self.scheme = helpers.build_scheme("instance/credentials")
        self.term = "public_key"
        self.path = "%s.credentials.publickey" % _OPENSTACK_PATH
        attrs = [
            attribute.InmutableAttribute(
                "%s.name" % self.path, name),
            attribute.InmutableAttribute(
                "%s.data" % self.path , data),
        ]

        attrs = attribute.AttributeCollection({a.name: a for a in attrs})

        super(OpenStackPublicKey, self).__init__(
            OpenStackPublicKey.scheme, OpenStackPublicKey.term,
            "Contextualization extension - public_key",
            attributes=attrs)

    @property
    def name(self):
        attr = "%s.name" % self.path
        return self.attributes[attr].value

    @property
    def data(self):
        attr = "%s..data" % self.path
        return self.attributes[attr].value


user_data = OpenStackUserData()
public_key = OpenStackPublicKey()
