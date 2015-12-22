Juno (2014.2)
-------------

.. code:: ini

[composite:neutron]
use = egg:Paste#urlmap
/: neutronversions
/v2.0: neutronapi_v2_0
/occinet0.1: occinet_api_01


....


[filter:occi]
paste.filter_factory = occinet.wsgi.middleware:OCCINetworkMiddleware.factory
openstack_version = /v2.0

[composite:occinet_api_01]
use = call:neutron.auth:pipeline_factory
noauth = request_id catch_errors extensions occi neutronapiapp_v2_0
keystone = request_id catch_errors authtoken keystonecontext extensions occi neutronapiapp_v2_0
