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
module: synapse_register
short_description: Register a synapse user
description:
    - register a matrix user using synapse's admin API
options:
    hs_url:
        description:
            - URL of the homeserver, where the CS-API is reachable
        required: true
        type: str
    user_id:
        description:
            - The user id of the user
        required: true
        type: str
    password:
        description:
            - The password to register with
        required: true
        type: str
    admin:
        description:
            - Whether or not the new user should be an admin
        required: false
        default: false
        type: bool
    shared_secret:
        description:
            - Shared secret to authenticate registration request
        required: true
        type: str
requirements: []
'''

EXAMPLES = '''
- name: Log in to matrix
  synapse_register:
    hs_url: "https://matrix.org"
    user_id: "{{ matrix_auth_user }}"
    password: "{{ matrix_auth_password }}"
    admin: true
    shared_secret: "long secret string"
'''

import asyncio
import hmac
import hashlib
import traceback

# Check if all required libs can load
LIB_IMP_ERR = None
try:
    import requests

    HAS_REQUESTS = True
except ImportError:
    REQUESTS_IMPORT_ERROR = traceback.format_exc()
    HAS_REQUESTS = False

from ansible.module_utils.basic import AnsibleModule, missing_required_lib


def generate_mac(nonce, shared_secret, user, password, admin=False, user_type=None):
    mac = hmac.new(
        key=shared_secret.encode('utf8'),
        digestmod=hashlib.sha1,
    )

    mac.update(nonce.encode('utf8'))
    mac.update(b"\x00")
    mac.update(user.encode('utf8'))
    mac.update(b"\x00")
    mac.update(password.encode('utf8'))
    mac.update(b"\x00")
    mac.update(b"admin" if admin else b"notadmin")
    if user_type:
        mac.update(b"\x00")
        mac.update(user_type.encode('utf8'))

    return mac.hexdigest()


async def run_module():
    module_args = dict(
        hs_url=dict(type='str', required=True),
        user_id=dict(type='str', required=True),
        password=dict(type='str', required=True, no_log=True),
        admin=dict(type='bool', required=False, default=False),
        shared_secret=dict(type='str', required=True, no_log=True),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not HAS_REQUESTS:
        module.fail_json(msg=missing_required_lib("requests"))

    if module.check_mode:
        return result

    failed = False

    url = f"{module.params['hs_url']}/_synapse/admin/v1/register"
    response = requests.get(url)
    if response.status_code != 200:
        result["msg"] = response.json()["error"]
        module.exit_json(**result)
    nonce = response.json()["nonce"]
    mac = generate_mac(nonce, module.params["shared_secret"], module.params["user_id"], module.params["password"],
                       module.params["admin"])

    data = {
        "nonce": nonce,
        "username": module.params["user_id"],
        "password": module.params["password"],
        "mac": mac,
        "admin": module.params["admin"],
    }

    response = requests.post(url, json=data)
    if response.status_code == 200:
        result["changed"] = True
    elif response.json()["errcode"] == "M_USER_IN_USE":
        result["changed"] = False
    else:
        result["msg"] = response.json()
        module.fail_json(**result)

    module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == '__main__':
    main()
