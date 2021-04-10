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
module: matrix_notification
short_description: Send notifications to matrix
description:
    - This module sends html formatted notifications to matrix rooms.
version_added: "2.8"
options:
    msg_plain:
        description:
            - Plain text form of the message to send to matrix, usually markdown
        required: true
    msg_html:
        description:
            - HTML form of the message to send to matrix
        required: true
    room_id:
        description:
            - ID of the room to send the notification to
        required: true
    hs_url:
        description:
            - URL of the homeserver, where the CS-API is reachable
        required: true
    token:
        description:
            - Authentication token for the API call. If provided, user_id and password are not required
    user_id:
        description:
            - The user id of the user
    password:
        description:
            - The password to log in with
requirements:
    -  matrix-nio (Python library)
'''

EXAMPLES = '''
- name: Send matrix notification with token
  matrix_notification:
    msg_plain: "**hello world**"
    msg_html: "<b>hello world</b>"
    room_id: "!12345678:server.tld"
    hs_url: "https://matrix.org"
    token: "{{ matrix_auth_token }}"

- name: Send matrix notification with user_id and password
  matrix_notification:
    msg_plain: "**hello world**"
    msg_html: "<b>hello world</b>"
    room_id: "!12345678:server.tld"
    hs_url: "https://matrix.org"
    user_id: "ansible_notification_bot"
    password: "{{ matrix_auth_password }}"
'''

RETURN = '''
'''
import traceback
import asyncio
from ansible_collections.famedly.matrix.plugins.module_utils.matrix import *

async def run_module():
    module_args = dict(
        msg_plain=dict(type='str', required=True),
        msg_html=dict(type='str', required=True),
        room_id=dict(type='str', required=True),
   )

    result = dict(
        changed=False,
        message=''
    )

    module = AnsibleNioModule(module_args)

    if module.check_mode:
        return result
    
    await module.matrix_login()
    client = module.client

    # send message
    await client.room_send(
        room_id=module.params['room_id'],
        message_type="m.room.message",
        content={
            "msgtype": "m.text",
            "body": module.params['msg_plain'],
            "format": "org.matrix.custom.html",
            "formatted_body": module.params['msg_html'],
        }
    )

    await module.exit_json(**result)

def main():
    asyncio.run(run_module())


if __name__ == '__main__':
    main()
