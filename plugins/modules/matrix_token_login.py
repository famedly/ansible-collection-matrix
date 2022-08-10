#!/usr/bin/python
# coding: utf-8

# (c) 2018, Jan Christian Grünhage <jan.christian@gruenhage.xyz>
# (c) 2020-2021, Famedly GmbH
# (c) 2022 Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

ANSIBLE_METADATA = {
    "metadata_version": "1.1",
    "status": ["preview"],
    "supported_by": "community",
}

DOCUMENTATION = """
---
author: "Jan Christian Grünhage (@jcgruenhage)"
module: matrix_token_login
short_description: Use com.famedly.token based logins to obtain an access token
description:
    - Log in to a matrix homeserver com.famedly.login for authentication and get an access token back
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
    key:
        description: Login key to use
        type: str
        required: true
    admin:
        description:
            - Whether to set the user as admin during login
        type: bool
requirements:
    -  matrix-nio (Python library)
    -  jwcrypto (Python library)
"""

EXAMPLES = """
- name: Log in to matrix
  matrix_token_login:
    hs_url: "https://example.famedly.care"
    user_id: "{{ matrix_user }}"
    admin: false
    key: "{{ matrix_token_login_key }}"
"""

RETURN = """
token:
  description: The access token aquired by logging in
  returned: When login was successful
  type: str
device_id:
  description: The device ID assigned by the server
  returned: When login was successful
  type: str
"""
import asyncio
import json
import base64
import time
import traceback

from ansible.module_utils.basic import missing_required_lib

# Check if all required libs can load
JWCRYPTO_IMP_ERR = None
try:
    from jwcrypto import jwt, jwk

    HAS_JWCRYPTO = True
except ImportError:
    JWCRYPTO_IMP_ERR = traceback.format_exc()
    HAS_JWCRYPTO = False

NIO_IMP_ERR = None
try:
    from ansible_collections.famedly.matrix.plugins.module_utils.matrix import (
        AnsibleNioModule,
    )
    from nio import AsyncClient, Api

    HAS_NIO = True
except ImportError:
    NIO_IMP_ERR = traceback.format_exc()
    HAS_NIO = False


async def run_module():
    module_args = dict(
        hs_url=dict(type="str", required=True),
        user_id=dict(type="str", required=True),
        key=dict(type="str", required=True, no_log=True),
        admin=dict(type="bool", required=False),
    )

    result = dict(
        changed=False,
        msg="",
    )

    args = {
        "add_default_arguments": False,
        "required_by": {},
        "required_one_of": [],
        "mutually_exclusive": [],
    }

    module = AnsibleNioModule(module_args, user_logout=False, **args)
    if not HAS_JWCRYPTO:
        await module.fail_json(msg=missing_required_lib("jwcrypto"))
    if not HAS_NIO:
        await module.fail_json(msg=missing_required_lib("matrix-nio"))

    if module.check_mode:
        return result

    failed = False

    # Create client object
    client = AsyncClient(module.params["hs_url"], module.params["user_id"])
    module.client = client

    # Collect and check login information
    key = module.params["key"]
    if key is None:
        await module.fail_json(msg="A key has to be provided")

    admin = module.params["admin"]

    method, path, data = Api.login(
        client.user,
        password="",
    )

    key = {
        # See rfc7518#section-6.4.1: k should contain the base64url encoded binary key.
        "k": base64.urlsafe_b64encode(key.encode("utf-8")).decode("utf-8"),
        "kty": "oct",
    }
    key = jwk.JWK(**key)
    claims = {
        "iss": "Matrix UIA Login Ansible Module",
        "sub": client.user,
        "exp": int(time.time()) + 60 * 30,
    }

    if admin is not None:
        claims["admin"] = admin

    token = jwt.JWT(header={"alg": "HS512"}, claims=claims)

    token.make_signed_token(key)

    auth = {
        "type": "com.famedly.login.token",
        "identifier": {"type": "m.id.user", "user": client.user},
        "token": token.serialize(),
    }

    payload = json.dumps(auth)

    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": str(len(payload)),
    }

    raw_response = await client.send(method, path, payload, headers)
    res = await client.parse_body(raw_response)

    if raw_response.status != 200:
        failed = True
        result["msg"] = await raw_response.text()
    else:
        result["token"] = res["access_token"]
        result["device_id"] = res["device_id"]

    if failed:
        await module.fail_json(**result)
    else:
        await module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == "__main__":
    main()
