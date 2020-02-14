#!/usr/bin/python
# coding: utf-8

# (c) 2018, Jan Christian Grünhage <jan.christian@gruenhage.xyz>
# (c) 2020, Famedly GmbH
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

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

MATRIX_IMP_ERR = None
try:
    from nio import AsyncClient
except ImportError:
    MATRIX_IMP_ERR = traceback.format_exc()
    matrix_found = False
else:
    matrix_found = True

async def run_module():
    module_args = dict(
        hs_url=dict(type='str', required=True),
        user_id=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not matrix_found:
        module.fail_json(msg=missing_required_lib('matrix-nio'), exception=MATRIX_IMP_ERR)

    if module.check_mode:
        return result

    # Create client object
    client = AsyncClient(module.params['hs_url'], module.params['user_id'])
    # Log in
    login_response = await client.login(module.params['password'])

    # Store results
    result['token'] = login_response.access_token
    result['device_id'] = login_response.device_id

    # Close client sessions
    await client.close()

    module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == '__main__':
    main()
