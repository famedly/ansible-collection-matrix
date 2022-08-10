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
module: matrix_member
short_description: Manage matrix room membership
description:
    - Manage the membership status of a given set of matrix users. Invitations (`state=member`),
      kicks and bans can be issued. With the `exclusive=True` flag, all other members in the room can be auto-kicked.
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
    room_id:
        description:
            - ID of the room to edit
        required: true
        type: str
    user_ids:
        description:
            - List of matrix IDs to set their state
        type: list
        elements: str
        required: true
    state:
        description:
            - In which state all listed members should be member|kicked|banned
        choices: ['member', 'kicked', 'banned']
        type: str
        required: true
    exclusive:
        description:
            - If state=member, the module ensure only the specified user_ids are in the room by
              kicking every other user present in the room.
        default: false
        type: bool
        required: false
requirements:
    -  matrix-nio (Python library)
"""

EXAMPLES = """
- name: Invite two users by matrix-ID into a room
  matrix_member:
    hs_url: "https://matrix.org"
    token: "{{ matrix_auth_token }}"
    room_id: "{{ matrix_room_id }}"
    state: member
    user_ids:
      - "@user1:matrix.org"
      - "@user2:homeserver.tld"
"""

RETURN = """
members:
  description: Dictionary of all members in the given room who are either invited or joined
  returned: When auth_token is valid
  type: dict
"""
import asyncio
import traceback
from ansible.module_utils.basic import missing_required_lib

LIB_IMP_ERR = None
try:
    from ansible_collections.famedly.matrix.plugins.module_utils.matrix import (
        AnsibleNioModule,
    )
    from nio import (
        RoomGetStateError,
        RoomBanError,
        RoomUnbanError,
        RoomKickError,
        RoomInviteError,
    )

    HAS_LIB = True
except ImportError:
    LIB_IMP_ERR = traceback.format_exc()
    HAS_LIB = False


class NioOperationError(Exception):
    def __init__(self, *args):
        super().__init__(*args)


async def get_room_members(client, room_id, res):
    member_resp = await client.room_get_state(room_id)

    if isinstance(member_resp, RoomGetStateError):
        res["msg"] = f"Could not get room state for roomId={room_id}"
        raise NioOperationError(res["msg"])
    else:
        return dict(
            list(
                map(
                    lambda m: (m["state_key"], m["content"]["membership"]),
                    filter(
                        lambda e: e["type"] == "m.room.member"
                        and e["content"]["membership"]
                        in ["invite", "join", "leave", "ban"],
                        member_resp.events,
                    ),
                )
            )
        )


async def ban_from_room(client, room_id, user_id, res):
    ban_resp = await client.room_ban(room_id, user_id)
    if isinstance(ban_resp, RoomBanError):
        res["msg"] = f"Could not ban user={user_id} from roomId={room_id}"
        raise NioOperationError(res["msg"])
    res["changed"] = True
    res["banned"].append(user_id)


async def unban_from_room(client, room_id, user_id, res):
    ban_resp = await client.room_unban(room_id, user_id)
    if isinstance(ban_resp, RoomUnbanError):
        res["msg"] = f"Could not unban user={user_id} from roomId={room_id}"
        raise NioOperationError(res["msg"])
    res["changed"] = True
    res["unbanned"].append(user_id)


async def kick_from_room(client, room_id, user_id, res):
    kick_resp = await client.room_kick(room_id, user_id)
    if isinstance(kick_resp, RoomKickError):
        res["msg"] = f"Could not kick user={user_id} from roomId={room_id}"
        raise NioOperationError(res["msg"])
    res["changed"] = True
    res["kicked"].append(user_id)


async def invite_to_room(client, room_id, user_id, res):
    invite_resp = await client.room_invite(room_id, user_id)
    if isinstance(invite_resp, RoomInviteError):
        res["msg"] = f"Could not invite user={user_id} to roomId={room_id}"
        raise NioOperationError(res["msg"])
    res["changed"] = True
    res["invited"].append(user_id)


async def run_module():
    module_args = dict(
        state=dict(choices=["member", "kicked", "banned"], required=True),
        room_id=dict(type="str", required=True),
        user_ids=dict(type="list", required=True, elements="str"),
        exclusive=dict(type="bool", required=False, default=False),
    )

    result = dict(
        changed=False,
        banned=[],
        unbanned=[],
        kicked=[],
        invited=[],
        members=[],
        msg="",
    )

    module = AnsibleNioModule(module_args)
    if not HAS_LIB:
        await module.fail_json(msg=missing_required_lib("matrix-nio"))

    await module.matrix_login()

    if module.check_mode:
        return result

    action = module.params["state"]
    room_id = module.params["room_id"]
    user_ids = module.params["user_ids"]

    # Check for valid parameter combination
    if module.params["exclusive"] and action != "member":
        await module.fail_json(msg="exclusive=True can only be used with state=member")

    # Create client object
    client = module.client

    try:
        # Query all room members (invited users count as member, as they _can_ be in the room)
        room_members = await get_room_members(client, room_id, result)
        present_members = {
            m: s for m, s in room_members.items() if s in ["join", "invite"]
        }.keys()
        banned_members = {m: s for m, s in room_members.items() if s == "ban"}.keys()
    except NioOperationError:
        await module.fail_json(**result)

    if not module.params["exclusive"]:
        # Handle non-exclusive invite|kick|ban
        try:
            for user_id in user_ids:
                if action == "member" and user_id not in present_members:
                    if user_id in banned_members:
                        await unban_from_room(client, room_id, user_id, result)
                    await invite_to_room(client, room_id, user_id, result)
                elif action == "kicked" and user_id in present_members:
                    await kick_from_room(client, room_id, user_id, result)
                elif action == "kicked" and user_id in banned_members:
                    await unban_from_room(client, room_id, user_id, result)
                elif action == "banned" and user_id not in banned_members:
                    await ban_from_room(client, room_id, user_id, result)
        except NioOperationError:
            await module.fail_json(**result)
    else:
        # Handle exclusive mode: get state and make lists of users to be kicked or invited
        to_invite = list(filter(lambda m: m not in present_members, user_ids))
        to_kick = list(filter(lambda m: m not in user_ids, present_members))

        try:
            for user_id in to_invite:
                await invite_to_room(client, room_id, user_id, result)
            for user_id in to_kick:
                await kick_from_room(client, room_id, user_id, result)
        except NioOperationError:
            await module.fail_json(**result)

    # Get all current members from the room
    try:
        room_members_after = await get_room_members(client, room_id, result)
        result["members"] = {
            m: s for m, s in room_members_after.items() if s in ["join", "invite"]
        }.keys()
    except NioOperationError:
        pass

    await module.exit_json(**result)


def main():
    asyncio.run(run_module())


if __name__ == "__main__":
    main()
