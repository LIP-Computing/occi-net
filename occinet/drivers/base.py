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

import copy
import json
import os

import six.moves.urllib.parse as urlparse

from ooi import exception
from ooi.log import log as logging
from ooi import utils

import webob.exc

LOG = logging.getLogger(__name__)


def _resolve_id(base_url, resource_url):
    """Gets the resource id from a base URL.

    :param base_url: application or request url (normally absolute)
    :param resource_url: absolute or relative resource url
    :returns: a tuple with the calculated base url and resource id
    """
    if not base_url.endswith('/'):
        base_url = base_url + '/'
    full_url = urlparse.urljoin(base_url, resource_url)
    parts = urlparse.urlsplit(full_url)
    base_parts = parts[0:2] + (os.path.dirname(parts[2]),) + parts[3:]
    return urlparse.urlunsplit(base_parts), os.path.basename(parts[2])


def get_id_with_kind(req, resource_url, kind=None):
    """Resolves the resource URL and tries to match it with the kind.

    :param req: current request
    :param resource_url: absolute or relative resource url
    :returns: a tuple with a base url and a resource id
    :raises ooi.exception.Invalid: if resource does not match kind
    """
    res_base, res_id = _resolve_id(req.url, resource_url)
    if kind:
        kind_base, kind_id = _resolve_id(req.application_url, kind.location)
        if kind_base != res_base:
            raise exception.Invalid("Expecting %s resource" % kind_base)
    return res_base, res_id


def exception_from_response(response):
    """Convert an OpenStack V2 Fault into a webob exception.

    Since we are calling the OpenStack API we should process the Faults
    produced by them. Extract the Fault information according to [1] and
    convert it back to a webob exception.

    [1] http://docs.openstack.org/developer/nova/v2/faults.html

    :param response: a webob.Response containing an exception
    :returns: a webob.exc.exception object
    """
    exceptions = {
        400: webob.exc.HTTPBadRequest,
        401: webob.exc.HTTPUnauthorized,
        403: webob.exc.HTTPForbidden,
        404: webob.exc.HTTPNotFound,
        405: webob.exc.HTTPMethodNotAllowed,
        406: webob.exc.HTTPNotAcceptable,
        409: webob.exc.HTTPConflict,
        413: webob.exc.HTTPRequestEntityTooLarge,
        415: webob.exc.HTTPUnsupportedMediaType,
        429: webob.exc.HTTPTooManyRequests,
        501: webob.exc.HTTPNotImplemented,
        503: webob.exc.HTTPServiceUnavailable,
    }
    code = response.status_int
    try:
        message = response.json_body.popitem()[1].get("message")
    except Exception:
        LOG.exception("Unknown error happenened processing response %s"
                      % response.body)
        return webob.exc.HTTPInternalServerError()

    exc = exceptions.get(code, webob.exc.HTTPInternalServerError)
    return exc(explanation=message)


class BaseHelper(object):
    """Base helper to interact with nova API."""
    def __init__(self, app, openstack_version):
        self.app = app
        self.openstack_version = openstack_version

    def _get_req(self, req, method,
                 path=None,
                 content_type="application/json",
                 body=None,
                 query_string=""):
        """Return a new Request object to interact with OpenStack.

        This method will create a new request starting with the same WSGI
        environment as the original request, prepared to interact with
        OpenStack. Namely, it will override the script name to match the
        OpenStack version. It will also override the path, content_type and
        body of the request, if any of those keyword arguments are passed.

        :param req: the original request
        :param path: new path for the request
        :param content_type: new content type for the request, defaults to
                             "application/json" if not specified
        :param body: new body for the request
        :param query_string: query string for the request, defaults to an empty
                             query if not specified
        :returns: a Request object
        """
        new_req = webob.Request(copy.copy(req.environ))
        new_req.script_name = self.openstack_version
        new_req.query_string = query_string
        new_req.method = method
        if path is not None:
            new_req.path_info = path
        if content_type is not None:
            new_req.content_type = content_type
        if body is not None:
            new_req.body = utils.utf8(body)

        return new_req

    @staticmethod
    def get_from_response(response, element, default):
        """Get a JSON element from a valid response or raise an exception.

        This method will extract an element a JSON response (falling back to a
        default value) if the response has a code of 200, otherwise it will
        raise a webob.exc.exception

        :param response: The webob.Response object
        :param element: The element to look for in the JSON body
        :param default: The default element to be returned if not found.
        """
        if response.status_int in [200, 201, 202, 204]:
            return response.json_body.get(element, default)
        else:
            raise exception_from_response(response)
