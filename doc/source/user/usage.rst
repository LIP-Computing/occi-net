Developer documentation
=======================


Network
*****************

Network management provides list, show, create and delete networks to a specific tenant.

List networks
------
It lists all networks available for connecting virtual machines of a tenant::

    curl -H "X-Auth-token: "$OS_TOKEN http://127.0.0.23:8787/occi1.1/network


It returns a HTTP 200 with output::

    X-OCCI-Location: http://127.0.0.23:8787/occi1.1/network/2c9868b4-f71a-45d2-ba8c-dbf42f0b3120
    X-OCCI-Location: http://127.0.0.23:8787/occi1.1/network/4213c7ef-68d4-42e8-a3cd-1c5bab3abe6
    X-OCCI-Location: http://127.0.0.23:8787/occi1.1/network/PUBLIC

Show network
------
It shows the network features::

    curl -H "X-Auth-token: "$OS_TOKEN http://127.0.0.23:8787/occi1.1/network/b8a3d813-65da-4910-a80c-f97b4ba31fd4



It returns a HTTP 200 with output::

    Category: network; scheme="http://schemas.ogf.org/occi/infrastructure#"; class="kind"; title="network resource";
     rel="http://schemas.ogf.org/occi/core#resource"; location="http://127.0.0.23:8787/occi1.1/network/"
    Category: ipnetwork; scheme="http://schemas.ogf.org/occi/infrastructure/network#"; class="mixin";
     title="IP Networking Mixin"
    Category: osnetwork; scheme="http://schemas.openstack.org/infrastructure/network#"; class="mixin";
     title="openstack network"
    X-OCCI-Attribute: occi.network.address="20.0.0.0/24"
    X-OCCI-Attribute: occi.network.state="active"
    X-OCCI-Attribute: occi.core.title="CommandLineOCCI"
    X-OCCI-Attribute: occi.network.gateway="20.0.0.1"
    X-OCCI-Attribute: occi.core.id="4a7dc666-33d2-495e-93fe-ccd224c98c11"
    Link: <http://127.0.0.23:8787/occi1.1/network/4a7dc666-33d2-495e-93fe-ccd224c98c11?action=up>;
     rel="http://schemas.ogf.org/occi/infrastructure/network/action#up"
    Link: <http://127.0.0.23:8787/occi1.1/network/4a7dc666-33d2-495e-93fe-ccd224c98c11?action=down>;
    rel="http://schemas.ogf.org/occi/infrastructure/network/action#down"

Create network
------
It shows the network features::

    curl -X POST http://127.0.0.23:8787/occi1.1/network/ -H 'X-Auth-Token: '$OS_TOKEN
      -H 'Category: network; scheme="http://schemas.ogf.org/occi/infrastrunfrastructure/network#";
      class="mixin"' -H 'Content-Type: text/occi' -H 'X-OCCI-Attribute: occi.core.title="CommandLineOCCI",
       occi.network.address="20.0.0.0/24"'

It returns a HTTP 201 with output::

    X-OCCI-Location: http://127.0.0.23:8787/occi1.1/network/4a7dc666-33d2-495e-93fe-ccd224c98c11

Delete network
------
It shows the network features::

    curl -X DELETE -H "X-Auth-token: "$OS_TOKEN http://127.0.0.23:8787/occi1.1/network/cb94496e-7e8e-4cb6-841d-30f38bc375e6

It returns a 204 empty response.

