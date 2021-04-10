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
module: matrix_logout
short_description: Log out of matrix
description:
    - Invalidate an access token by logging out
options:
    hs_url:
        description:
            - URL of the homeserver, where the CS-API is reachable
        required: true
    token:
        description:
            - Authentication token for the API call
        required: true
requirements:
    -  matrix-nio (Python library)
'''

EXAMPLES = '''
- name: Invalidate access token
  matrix_logout:
    hs_url: "https://matrix.org"
    token: "{{ matrix_auth_token }}"
'''

RETURN = '''
'''
import traceback
import asyncio

from ansible_collections.famedly.matrix.plugins.module_utils.matrix import *
async def run_module():
    result = dict(
        changed=False,
    )

    module = AnsibleNioModule()
    await module.matrix_login()
    await module.matrix_logout()
    await module.exit_json(**result)


def main():
    asyncio.run(run_module())

if __name__ == '__main__':
    main()
