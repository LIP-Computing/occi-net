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
#

from ooi.wsgi import parsers


class ParserNet (parsers.HeaderParser):

    def __init__(self, headers, body):
        super(ParserNet, self).__init__(headers, body)

    def get_attributes_from_dict(self):
        parameters = {}
        for key in self.headers['HTTP_X_OCCI_ATTRIBUTE'].keys():
            parameters[key]= self.headers['HTTP_X_OCCI_ATTRIBUTE'][key]

        return parameters

    def get_attributes_from_headers(self):
        #attr = self.parse_attributes(self.headers)
        attrs = None
        if 'HTTP_X_OCCI_ATTRIBUTE' in self.headers:
            attrs = {}
            try:
                header_attrs = self.headers["HTTP_X_OCCI_ATTRIBUTE"]
                for attr in parsers._quoted_split(header_attrs):
                    l = parsers._split_unquote(attr)
                    attrs[l[0].strip()] = l[1]
            except KeyError:
                pass

        return attrs

    def get_attributes_from_headers(self):
        #attr = self.parse_attributes(self.headers)
        attrs = None
        if 'HTTP_X_OCCI_ATTRIBUTE' in self.headers:
            attrs = {}
            try:
                header_attrs = self.headers["HTTP_X_OCCI_ATTRIBUTE"]
                for attr in parsers._quoted_split(header_attrs):
                    l = parsers._split_unquote(attr)
                    attrs[l[0].strip()] = l[1]
            except KeyError:
                pass

        return attrs


def make_body(parameters):
        body = {"network":{}}
        for key in parameters.keys():
            body["network"][key] = parameters[key]

        return body


def get_query_string(parameters):
        query_string = ""
        if parameters is None:
            return None

        for key in parameters.keys():
            query_string = ("%s%s=%s&" % (query_string, key, parameters[key]))

        return query_string[:-1] # delete last character


def translate_parameters(translation, parameters):
    if not parameters:
        return parameters
    out = {}
    for key in parameters.keys():
        if key in translation:
            out[translation[key]] = parameters[key]
    return out


def network_status(neutron_status):
    if neutron_status == "ACTIVE":
        return "active"
    elif neutron_status == "SUSPENDED":
        return "suspended"
    else:
        return "inactive"