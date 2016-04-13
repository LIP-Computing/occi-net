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

from ooi.api import base
from ooi.api import helpers
from ooi.api import network as network_api
from ooi import exception
from ooi.occi.core import collection
from ooi.occi.infrastructure import compute
from ooi.occi.infrastructure import network
from ooi.occi.infrastructure import network_link
from ooi.occi import validator as occi_validator
from ooi.openstack import network as os_network


class Controller(base.Controller):
    def __init__(self, neutron_endpoint):
        self.os_neutron_helper = helpers.OpenStackNet(
            neutron_endpoint
        )

    @staticmethod
    def _get_network_link_resources(link_list):
        """Create networkLink instances from network in json format

        :param link_list: provides by the cloud infrastructure
        """
        occi_network_resources = []
        if link_list:
            for l in link_list:
                compute_id = l['compute_id']
                mac = l["mac"]
                net_pool = l['pool']
                ip = l['ip']
                state = l['state']
                if net_pool: # mac only in the public
                    net_id = network_api.PUBLIC_NETWORK
                else:
                    net_id = l['network_id']
                n = network.NetworkResource(title="network",
                                            id=net_id)
                c = compute.ComputeResource(title="Compute",
                                            id=compute_id
                                            )
                iface = os_network.OSNetworkInterface(c, n, mac, ip,
                                                      pool=net_pool,
                                                      state=state)
                occi_network_resources.append(iface)
        return occi_network_resources

    def _get_interface_from_id(self, req, id):
        try:
            server_id, network_id, server_addr = id.split('_', 2)
        except ValueError:
            raise exception.LinkNotFound(link_id=id)
        try:
            link = self.os_neutron_helper.get_compute_net_link(
                req,
                server_id,
                network_id,
                server_addr)
        except:
            raise exception.LinkNotFound(link_id=id)
        occi_list = self._get_network_link_resources([link])
        return occi_list

    def index(self, req):
        attributes = network_api.filter_attributes(req)
        link_list = self.os_neutron_helper.list_compute_net_links(req, attributes)
        occi_link_resources = self._get_network_link_resources(link_list)
        return collection.Collection(resources=occi_link_resources)

    def show(self, req, id):
        return self._get_interface_from_id(req, id)

    def create(self, req, body):
        parser = req.get_parser()(req.headers, req.body)
        scheme = {
            "category": network_link.NetworkInterface.kind,
            "optional_mixins": [
                os_network.OSFloatingIPPool,
            ]
        }
        obj = parser.parse()
        validator = occi_validator.Validator(obj)
        validator.validate(scheme)

        attrs = obj.get("attributes", {})
        _, net_id = helpers.get_id_with_kind(
            req,
            attrs.get("occi.core.target"),
            network.NetworkResource.kind)
        _, server_id = helpers.get_id_with_kind(
            req,
            attrs.get("occi.core.source"),
            compute.ComputeResource.kind)

        # todo(jorgesece): check if about pools
        pool_name = None
        if os_network.OSFloatingIPPool.scheme in obj["schemes"]:
            pool_name = obj["schemes"][os_network.OSFloatingIPPool.scheme][0]

        # Allocate public IP and associate it ot the server
        if net_id == network_api.PUBLIC_NETWORK:
            os_link = self.os_neutron_helper.assign_floating_ip(
                req,
                server_id)
        else:
            # Allocate private network
            os_link = self.os_neutron_helper.create_port(
                req,
                net_id,
                server_id)
            # raise exception.NetworkNotFound(resource_id=net_id)

        occi_link = self._get_network_link_resources([os_link])
        return collection.Collection(resources=[occi_link])

    def delete(self, req, id):
        iface = self._get_interface_from_id(req, id)[0]
        if iface.target.id == network_api.PUBLIC_NETWORK:
            os_link = self.os_neutron_helper.release_floating_ip(
                req, iface.source.id)
        else:
            os_link = self.os_neutron_helper.delete_port(iface.mac)
        return []
