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
    def __init__(self, app, openstack_version, neutron_endpoint):
        super(Controller, self).__init__(app, openstack_version)
        self.os_helper = helpers.OpenStackHelper(
            self.app,
            self.openstack_version
        )
        self.os_neutron_helper = helpers.OpenStackNet(
            neutron_endpoint
        )

    def index2(self, req):
        floating_ips = self.os_helper.get_floating_ips(req)
        occi_link_resources = []
        for ip in floating_ips:
            parameters = {'devide_id=%s' % ip['instance_id']}
            ports = self.os_neutron_helper.get_ports(req, parameters)
            if ports.__len__() > 0:
                net_id = ports[0]["network_id"]
                n = network.NetworkResource(title="network",
                                            id=net_id)
                c = compute.ComputeResource(title="Compute",
                                            id=ip["instance_id"])
                # TODO(enolfc): get the MAC?
                iface = os_network.OSNetworkInterface(c, n, "mac", ip["ip"],
                                                      pool=ip["pool"])
# {"ports": [{"status": "ACTIVE", "binding:host_id": "ubuntu", "allowed_address_pairs": [], "extra_dhcp_opts": [],
#  "device_owner": "compute:nova", "binding:profile": {}, "fixed_ips": [{"subnet_id": "4bebdd47-215c-44a7-9a15-4f0ffdd7897d", "ip_address": "11.0.0.5"}],
#  "id": "838781e8-693d-40e7-b3f5-f698985a6ac0", "security_groups": ["8830f4f5-e18a-48af-a5ba-0543ca699938"],
#  "device_id": "1226a4c0-4190-46f6-a674-763c196ea18d", "name": "", "admin_state_up": true, "network_id": "2c9868b4-f71a-45d2-ba8c-dbf42f0b3120",
#  "tenant_id": "86bf9730b23d4817b431f4c34cc9cc8e", "binding:vif_details": {"port_filter": true, "ovs_hybrid_plug": true}, "binding:vnic_type": "normal",
#   "binding:vif_type": "ovs", "mac_address": "fa:16:3e:65:f3:6d"}]}

    def index(self, req):
        # FIXME(jorgesece): include every IP linked with VMs
        floating_ips = self.os_helper.get_floating_ips(req)
        occi_link_resources = []
        for ip in floating_ips:
            if ip["instance_id"]:
                # FIXME(jorgesece): create the full network
                n = network.NetworkResource(title="network",
                                            id=network_api.FLOATING_PREFIX)
                c = compute.ComputeResource(title="Compute",
                                            id=ip["instance_id"])
                # TODO(enolfc): get the MAC?
                iface = os_network.OSNetworkInterface(c, n, "mac", ip["ip"],
                                                      pool=ip["pool"])
                occi_link_resources.append(iface)

        return collection.Collection(resources=occi_link_resources)

    def _build_os_net_iface(self, req, server_id, addr):
        ip_id = pool = None
        if addr["OS-EXT-IPS:type"] == "fixed":
            net_id = network_api.FIXED_PREFIX
        else:
            net_id = network_api.FLOATING_PREFIX
            # FIXME(jorgesece): include every IP linked with VMs
            # TODO(jorgesece):  get server from id, an then network
            floating_ips = self.os_helper.get_floating_ips(req)
            for ip in floating_ips:
                if addr["addr"] == ip["ip"]:
                    ip_id = ip["id"]
                    pool = ip["pool"]
                    break
            else:
                raise exception.NetworkNotFound(resource_id=addr)
        c = compute.ComputeResource(title="Compute", id=server_id)
        n = network.NetworkResource(title="network", id=net_id)
        # TODO(enolfc): get the MAC?
        # FIXME(jorgesece): create the full network
        return os_network.OSNetworkInterface(c, n, "mac", addr["addr"],
                                             ip_id, pool)

    def _get_interface_from_id(self, req, id):
        try:
            server_id, server_addr = id.split('_', 1)
        except ValueError:
            raise exception.LinkNotFound(link_id=id)
        s = self.os_helper.get_server(req, server_id)
        addresses = s.get("addresses", {})
        for addr_set in addresses.values():
            for addr in addr_set:
                if addr["addr"] == server_addr:
                    return self._build_os_net_iface(req, server_id, addr)
        raise exception.LinkNotFound(link_id=id)

    def show(self, req, id):
        return [self._get_interface_from_id(req, id)]

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

        # net_id is something like "fixed" or "floating"
        if net_id == network_api.FIXED_PREFIX:
            raise exception.Invalid()
        elif net_id != network_api.FLOATING_PREFIX:
            raise exception.NetworkNotFound(resource_id=net_id)

        pool_name = None
        if os_network.OSFloatingIPPool.scheme in obj["schemes"]:
            pool_name = obj["schemes"][os_network.OSFloatingIPPool.scheme][0]
        # Allocate IP
        ip = self.os_helper.allocate_floating_ip(req, pool_name)

        # Add it to server
        # FIXME(jorgesece): include FIXED IP linked with VMs
        # TODO(jorgesece):  get server from id, an then network
        # FIXME(jorgesece): create the full network
        self.os_helper.associate_floating_ip(req, server_id, ip["ip"])
        n = network.NetworkResource(title="network", id=net_id)
        c = compute.ComputeResource(title="Compute", id=server_id)
        l = os_network.OSNetworkInterface(c, n, "mac", ip["ip"])
        return collection.Collection(resources=[l])

    def delete(self, req, id):
        iface = self._get_interface_from_id(req, id)
        if iface.target.id == "fixed":
            raise exception.Invalid()

        # remove floating IP
        server = iface.source.id
        # FIXME(jorgesece): include FIXED IP linked with VMs
        self.os_helper.remove_floating_ip(req, server, iface.address)

        # release IP
        self.os_helper.release_floating_ip(req, iface.ip_id)
        return []
