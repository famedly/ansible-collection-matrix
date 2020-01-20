#!/usr/bin/python
# coding: utf-8

# (c) 2018, Jan Christian Grünhage <jan.christian@gruenhage.xyz>
# (c) 2020, Famedly GmbH
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

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
module: matrix
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
    -  matrix-client (Python library)
'''

EXAMPLES = '''
- name: Invalidate access token
  matrix:
    hs_url: "https://matrix.org"
    token: "{{ matrix_auth_token }}"
'''

RETURN = '''
'''
import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

MATRIX_IMP_ERR = None
try:
    from matrix_client.client import MatrixClient
except ImportError:
    MATRIX_IMP_ERR = traceback.format_exc()
    matrix_found = False
else:
    matrix_found = True


def run_module():
    module_args = dict(
        hs_url=dict(type='str', required=True),
        token=dict(type='str', required=True, no_log=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not matrix_found:
        module.fail_json(msg=missing_required_lib('matrix-client'), exception=MATRIX_IMP_ERR)

    if module.check_mode:
        return result

    # create a client object
    client = MatrixClient(module.params['hs_url'])
    client.api.token = module.params['token']

    client.logout()

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
