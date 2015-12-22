Configuration
=============

Paste Configuration
*******************

TL;DR.
------

Add the corresponding Paste configuration according to your OpenStack version
from :ref:`pipeline-examples` into your Paste configuration file
(usually ``/etc/neutron/api-paste.ini``).

Detailed instructions

---------------------
Once installed it is needed to add it to your OpenStack installation. Edit your
``/etc/nova/api-paste.ini``.

First it is needed to add the OCCI filter like this::

    [filter:occi]
    paste.filter_factory = occinet.wsgi.middleware:OCCINetworkMiddleware.factory
    openstack_version = /v2.0

``openstack_version`` can be configured to any of the supported OpenStack API
versions, as indicated in Table :ref:`api-versions`. If it is not configured,
by default it will take the ``/v2.1`` value.

.. _api-versions:

.. table:: Supported OpenStack API versions

    ===================== ===================== =============================================
    OpenStack API version ``openstack_version`` reference OpenStack ``composite`` section
    ===================== ===================== =============================================
    v2                    ``/v2.0``               ``[composite:neutronapi_v2_0]``
    ===================== ===================== =============================================

The next step is to create a ``composite`` section for the OCCI interface. It
is needed to duplicate the :ref:`corresponding OpenStack API ``composite``<api-versions>` section,
renaming it to ``occinet_api_01``. Once duplicated, the ``occi`` middleware needs
to be added just before the last component of the pipeline. So, in the example
above where ``/v2.0`` has been configured, we need to duplicate the
``[composite:neutronapi_v2_0]`` as follows::

    [composite:occinet_api_01]
    use = call:neutron.auth:pipeline_factory
    noauth = request_id catch_errors extensions occi neutronapiapp_v2_0
    keystone = request_id catch_errors authtoken keystonecontext extensions occi neutronapiapp_v2_0


If everything is OK, after rebooting the ``neutron-services`` service you should be able
to access your OCCI endpoint at::

    $ export KID=<token>
    $ curl -H "x-auth-token: $KID" http://localhost:9696/occi1.1/-/

