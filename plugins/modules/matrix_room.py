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
author: "Jan Christian Grünhage (@jcgruenhage)"
module: matrix_room
short_description: Join/Create matrix room
description:
    - This module takes a room alias and makes sure that the user identified by the access token is in such a room.
      If that room does not exist, it is created, if it does exist but the user is not in it, it tries to join.
      If the alias is taken and the user can't join the room, the module will fail.
      Remote aliases are not supported for creating, but work for joining.
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
    alias:
        description:
            - Alias of the room to join/create
        required: true
        type: str
    no_create:
        description:
            - Prevent creation of room
        required: false
        default: false
        type: bool
    no_join:
        description:
            - Prevent joining of room
        required: false
        default: false
        type: bool
requirements:
    -  matrix-nio (Python library)
"""

EXAMPLES = """
- name: Create notification room
  matrix_room:
    alias: "#ansible-notifications:matrix.org"
    hs_url: "https://matrix.org"
    token: "{{ matrix_auth_token }}"
"""

RETURN = """
room_id:
  description: ID of the room
  type: str
  returned: success
  sample: "!asdfbuiarbk213e479asf:server.tld"
"""

import asyncio
import re
import traceback

from ansible.module_utils.basic import missing_required_lib

LIB_IMP_ERR = None
try:
    from ansible_collections.famedly.matrix.plugins.module_utils.matrix import (
        AnsibleNioModule,
    )
    from nio import (
        RoomCreateResponse,
        RoomCreateError,
        JoinedRoomsResponse,
        JoinedRoomsError,
        JoinResponse,
        JoinError,
        RoomResolveAliasResponse,
        RoomResolveAliasError,
    )

    HAS_LIB = True
except ImportError:
    LIB_IMP_ERR = traceback.format_exc()
    HAS_LIB = False


async def run_module():
    module_args = dict(
        alias=dict(type="str", required=True),
        no_create=dict(type="bool", required=False, default=False),
        no_join=dict(type="bool", required=False, default=False),
    )

    result = dict(changed=False, message="")

    module = AnsibleNioModule(module_args)
    if not HAS_LIB:
        await module.fail_json(msg=missing_required_lib("matrix-nio"))

    await module.matrix_login()
    client = module.client

    if module.check_mode:
        result["changed"] = True
        result["room_id"] = "!fakeRoomId:localhost"
        await module.exit_json(**result)

    # Try to look up room_id
    room_id_resp = await client.room_resolve_alias(module.params["alias"])

    failed = False
    result = {}

    if isinstance(room_id_resp, RoomResolveAliasResponse):
        # Check if already in room
        rooms_resp = await client.joined_rooms()
        if isinstance(rooms_resp, JoinedRoomsError):
            failed = True
            result = {"msg": "Couldn't get joined rooms."}
        elif room_id_resp.room_id in rooms_resp.rooms:
            result = {"room_id": room_id_resp.room_id, "changed": False}
        elif module.params["no_join"]:
            failed = True
            result = {
                "msg": "Room exists, we aren't a member of it, but joining was explicitly disabled"
            }
        else:
            # Try to join room
            join_resp = await client.join(module.params["alias"])

            # If successful, return, changed=true
            if isinstance(join_resp, JoinResponse):
                result = {"room_id": join_resp.room_id, "changed": True}
            else:
                failed = True
                result = {"msg": f"Room exists, but couldn't join: {join_resp}"}
    else:
        if module.params["no_create"]:
            failed = True
            result = {
                "msg": "Room doesn't exist, but room creation was explicitly disabled"
            }
        else:
            # Get local part of alias
            local_part_regex = re.search("#([^:]*):(.*)", module.params["alias"])
            local_part = local_part_regex.groups()[0]

            # Try to create room with alias
            create_room_resp = await client.room_create(alias=local_part)

            # If successful, exit with changed=true and room_id
            if isinstance(create_room_resp, RoomCreateResponse):
                result = {"room_id": create_room_resp.room_id, "changed": True}
            else:
                failed = True
                result = {
                    "msg": f"Room does not exist but couldn't be created either: {create_room_resp}"
                }
    if failed:
        await module.fail_json(**result)
    else:
        await module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == "__main__":
    main()
