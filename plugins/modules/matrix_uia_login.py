#!/usr/bin/python
# coding: utf-8

# (c) 2018, Jan Christian Grünhage <jan.christian@gruenhage.xyz>
# (c) 2020-2021, Famedly GmbH
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
author: "Johanna Dorothea Reichmann (@transcaffeine)"
module: matrix_uia_login
short_description: Use UIA against /login to obtain an access token
description:
    - Log in to a matrix homeserver using UIA and get an access token back
options:
    hs_url:
        description:
            - URL of the homeserver, where the CS-API is reachable
        required: true
        type: str
    user_id:
        description:
            - The user id of the user
        required: false
        type: str
    password:
        description:
            - The password to log in with
        required: false
        type: str
    token:
        description:
            - Authentication token for the API call
        required: false
        type: str
requirements:
    -  matrix-nio (Python library)
"""

EXAMPLES = """
- name: Log in to matrix
  matrix_uia_login:
    hs_url: "https://matrix.org"
    user_id: "{{ matrix_auth_user }}"
    password: "{{ matrix_auth_password }}"
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
import traceback

from ansible.module_utils.basic import missing_required_lib

LIB_IMP_ERR = None
try:
    from ansible_collections.famedly.matrix.plugins.module_utils.matrix import (
        AnsibleNioModule,
    )
    from nio import AsyncClient, Api

    HAS_LIB = True
except ImportError:
    LIB_IMP_ERR = traceback.format_exc()
    HAS_LIB = False

log = []


def get_payload(data):
    payload = json.dumps(data)
    payload_length = len(payload)
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Content-Length": str(payload_length),
    }
    return payload, headers


async def do_password_stage(client, session, method, path, password):
    auth = {
        "type": "m.login.password",
        "identifier": {"type": "m.id.user", "user": client.user},
        "session": session,
        "password": password,
    }
    log.append(
        f"DEBUG: attempt stage={auth['type']} for session={auth['session']} with password={auth['password']}, method={method}"
    )
    payload, headers = get_payload({"auth": auth})
    raw_response = await client.send(method, path, payload, headers)
    res = await client.parse_body(raw_response)
    log.append(f"DEBUG: stage={auth['type']} resulted in status={raw_response.status}")
    return raw_response.status, res


async def do_dummy_stage(client, session, method, path, password):
    auth = {"type": "m.login.dummy", "session": session}
    log.append(f"DEBUG: attempt stage={auth['type']} for session={auth['session']}")
    payload, headers = get_payload({"auth": auth})
    raw_response = await client.send(method, path, payload, headers)
    res = await client.parse_body(raw_response)
    log.append(f"DEBUG: stage{auth['type']} resulted in status={raw_response.status}")
    return raw_response.status, res


uia_stages = {"m.login.password": do_password_stage, "m.login.dummy": do_dummy_stage}


# Picks the best compatible flow out of an array of flows
def pick_flow(flows):
    supported_stages = uia_stages.keys()
    # reduces each flow to a boolean telling filter if the flow consists only out of compatible stages
    compatible_flows = [
        flow
        for flow in flows
        if all(stage in supported_stages for stage in flow["stages"])
    ]
    # the best flow is the one with the fewest stages, key= takes a function telling min() the weight of an entry
    best = min(compatible_flows, key=(lambda flow: len(flow["stages"])))
    return best


async def run_module():
    result = dict(
        changed=False,
    )

    module = AnsibleNioModule(user_logout=False)
    if not HAS_LIB:
        await module.fail_json(msg=missing_required_lib("matrix-nio"))

    if module.check_mode:
        return result

    failed = False

    # Create client object
    client = AsyncClient(module.params["hs_url"], module.params["user_id"])
    module.client = client

    # Collect and check login information
    password = module.params["password"]
    token = module.params["token"]
    if password is None and token is None:
        await module.fail_json(msg="A PASSWORD has to be provided")

    method, path, data = Api.login(
        client.user,
        password=password,
        device_name="",
        device_id=client.device_id,
        token=None,
    )

    # Send an empty POST to retrieve session and flow options
    raw_response = await client.send(method, path, {})
    res = await client.parse_body(raw_response)
    uia_session = res["session"]
    log.append(f"DEBUG: begin UIA for session={uia_session}")

    # Figure out best compatible UIA login flow
    log.append(f"INFO: available flows: {res['flows']}")
    flow_to_attempt = pick_flow(res["flows"])
    log.append(f"INFO: picking flow: {' -> '.join(flow_to_attempt['stages'])}")

    # Attempt each stage in the flow
    for stage in flow_to_attempt["stages"]:
        stage_status, stage_result = await uia_stages[stage](
            client, uia_session, method, path, password
        )
        if int(stage_status) == 401 and stage != (flow_to_attempt["stages"])[-1]:
            log.append(f"INFO: completed stage {stage}")
            stage_result["completed"]
        elif int(stage_status) == 200 and stage == (flow_to_attempt["stages"])[-1]:
            log.append(f"INFO: final stage completed {stage}")
            result["token"] = stage_result["access_token"]
            result["device_id"] = stage_result["device_id"]
            failed = False
        else:
            failed = True
            result["http_status_code"] = stage_status

    # Close client sessions
    result["msg"] = "\n".join(log)

    if failed:
        await module.fail_json(**result)
    else:
        await module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == "__main__":
    main()
