# -*- coding: utf-8 -*-

# Copyright 2015 Spanish National Research Council
# Copyright 2016 LIP - Lisbon
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

import ooi.api.base

from ooi.api import helpers
from ooi import exception
from ooi.occi.core import collection
from ooi.occi.infrastructure import network
from ooi.occi import validator as occi_validator
from ooi.openstack import network as os_network
from ooi import utils


PUBLIC_NETWORK = "PUBLIC"


def parse_validate_schema(req, scheme=None):
    """Parse attributes, even Validate scheme


    Returns attributes from request
    If scheme is specified, it validate the OCCI scheme:
     -Raises exception in case of being invalid

    :param req: request
    :param: scheme: scheme to validate
    """
    parser = req.get_parser()(req.headers, req.body)
    if scheme:
        attributes = parser.parse()
        validator = occi_validator.Validator(attributes)
        validator.validate(scheme)
    else:
        attributes = parser.parse_attributes(req.headers)
    return attributes


def process_parameters(req, scheme=None):
    """Get attributes from request parameters

    :param req: request
    :param: scheme: scheme to validate
    """
    parameters = parse_validate_schema(req, scheme)
    try:
        attributes = {}
        if 'X_PROJECT_ID' in req.headers:
            attributes["X_PROJECT_ID"] = req.headers["X_PROJECT_ID"]
        if "attributes" in parameters:
            for k, v in parameters.get("attributes", None).items():
                attributes[k.strip()] = v.strip()
        if not attributes:
            attributes = None
    except Exception:
        raise exception.Invalid
    return attributes


class Controller(ooi.api.base.Controller):
    def __init__(self, neutron_endpoint):
        super(Controller, self).__init__(app=None, openstack_version="v2.0")
        self.os_helper = helpers.OpenStackNet(
            neutron_endpoint
        )

    @staticmethod
    def _validate_attributes(required, attributes):
        """Get attributes from request parameters

        :param required: required attributes
        :param attributes: request attributes
        """
        for at in required:
            if at not in attributes:
                raise exception.Invalid()

    @staticmethod
    def _get_network_resources(networks_list):
        """Create network instances from network in json format

        :param networks_list: networks objects provides by the cloud infrastructure
        """
        occi_network_resources = []
        if networks_list:
            for s in networks_list:
                s["status"] = utils.network_status(s["status"])
                n_id = s["id"]
                n_status = s["status"]
                n_name = s["name"]
                if "subnet_info" in s:
                    # fixme(jorgesece) only works with the first subnetwork
                    n_cidr = s["subnet_info"]["cidr"]
                    n_ip_version = s["subnet_info"]["ip_version"]
                    n_gateway = s["subnet_info"]["gateway_ip"]
                    s = os_network.OSNetworkResource(title=n_name,
                                                     id=n_id, state=n_status,
                                                     ip_version=n_ip_version,
                                                     address=n_cidr,
                                                     gateway=n_gateway)
                else:
                    # FIXME(jorgesece): raise exception.NotFound()
                    # CHANGE IN TESTS
                    s = network.NetworkResource(title=n_name,
                                               id=n_id, state=n_status)
                occi_network_resources.append(s)
        return occi_network_resources

    def index(self, req):
        """List networks

        :param req: request object
        """
        attributes = process_parameters(req)
        occi_networks = self.os_helper.index(req, attributes)
        occi_network_resources = self._get_network_resources(
            occi_networks)

        return collection.Collection(
            resources=occi_network_resources)

    def show(self, req, id):
        """Get network details

        :param req: request object
        :param id: network identification
        """
        resp = self.os_helper.get_network_details(req, id)
        occi_network_resources = self._get_network_resources(
            [resp])
        return occi_network_resources[0]

    def create(self, req, body=None):
        """Create a network instance in the cloud

        :param req: request object
        :param body: body request (not used)
        """
        scheme = {
            "category": network.NetworkResource.kind,
            "optional_mixins": [
                network.ip_network,
            ]
        }
        attributes = process_parameters(req, scheme)
        self._validate_attributes(
            self.os_helper.required["networks"], attributes)
        net = self.os_helper.create_network(req, attributes)
        occi_network_resources = self._get_network_resources([net])
        return occi_network_resources[0]

    def delete(self, req, id):
        """delete networks which satisfy the parameters

        :param req: current request
        :param id: identification
        """
        response = self.os_helper.delete_network(req, id)
        return response

    def run_action(self, req, id, body, parameters=None):
        raise exception.NotFound()
