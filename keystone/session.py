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

from keystoneclient import session
from keystoneclient.v2_0 import client

from keystoneclient.auth.identity import v3

from keystonemiddleware import auth_token


class KeySession(object):

    def __init__(self, auth_url = 'http://localhost:5000/v2.0'):
        self.auth_url = auth_url

    def create_session(self, user, password, project):
        auth = v3.Password(auth_url=self.auth_url,
                           username=user,
                           password=password,
                           project_id=project)
        return session.Session(auth=auth)

    def create_keystone(self, user, password, project):
       #session = self.create_session(user, password, project)
       auth_token()
        keystone = client.Client(auth_url=self.auth_url,
                                 username=user,
                                 password=password,
                                 project_id=project)

        return keystone