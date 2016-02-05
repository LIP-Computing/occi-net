import abc

import six

@six.add_metaclass(abc.ABCMeta)
class Controller(object):
    def __init__(self, app, openstack_version):
        self.app = app
        self.openstack_version = openstack_version

