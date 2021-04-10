#!/usr/bin/python
# coding: utf-8

# (c) 2018, Jan Christian Grünhage <jan.christian@gruenhage.xyz>
# (c) 2020-2021, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
author: "Jan Christian Grünhage (@jcgruenhage)"
module: matrix_login
short_description: Get a matrix access token
description:
    - Log in to a matrix homeserver and get an access token back
options:
    hs_url:
        description:
            - URL of the homeserver, where the CS-API is reachable
        required: true
    user_id:
        description:
            - The user id of the user
        required: true
    password:
        description:
            - The password to log in with
        required: true
requirements:
    -  matrix-nio (Python library)
'''

EXAMPLES = '''
- name: Log in to matrix
  matrix_login:
    hs_url: "https://matrix.org"
    user_id: "{{ matrix_auth_user }}"
    password: "{{ matrix_auth_password }}"
'''

RETURN = '''
token:
  description: The access token aquired by logging in
  returned: When login was successful
  type: str
device_id:
  description: The device ID assigned by the server
  returned: When login was successful
  type: str
'''
import traceback
import asyncio

from ansible_collections.famedly.matrix.plugins.module_utils.matrix import *

async def run_module():
    result = dict(
        changed=False,
    )

    module = AnsibleNioModule(user_logout=False)
    await module.matrix_login()
    result['token'] = module.access_token
    result['device_id'] = module.device_id
    await module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == '__main__':
    main()
