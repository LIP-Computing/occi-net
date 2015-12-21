Kilo (2015.1)
-------------

.. code:: ini

[filter:occi]
paste.filter_factory = occinet.wsgi.middleware:OCCINetworkMiddleware.factory
openstack_version = /v2.1

[composite:occinet_api_01]
use = call:nova.api.auth:pipeline_factory
noauth = compute_req_id faultwrap sizelimit noauth ratelimit occi osapi_compute_app_v21
keystone = compute_req_id faultwrap sizelimit authtoken keystonecontext ratelimit occi osapi_compute_app_v21
keystone_nolimit = compute_req_id faultwrap sizelimit authtoken keystonecontext occi osapi_compute_app_v21

[composite:occinet]
use = call:nova.api.openstack.urlmap:urlmap_factory
/occinet0.1: occinet_api_01
