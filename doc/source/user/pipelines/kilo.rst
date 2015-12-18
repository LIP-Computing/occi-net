Kilo (2015.1)
-------------

.. code:: ini

    [composite:occinet]
    use = call:nova.api.openstack.urlmap:urlmap_factory
    /occinet0.1: occinet_api_01

    [filter:occinet]
    paste.filter_factory = occinet.wsgi.middleware:OCCINetworkMiddleware.factory
    openstack_version = /v2.1

    [composite:occinet_api_11]
    use = call:nova.api.auth:pipeline_factory_v21
    noauth = compute_req_id faultwrap sizelimit noauth occi osapi_compute_app_v21
    noauth2 = compute_req_id faultwrap sizelimit noauth2 occi osapi_compute_app_v21
    keystone = compute_req_id faultwrap sizelimit authtoken keystonecontext occinet osapi_compute_app_v21