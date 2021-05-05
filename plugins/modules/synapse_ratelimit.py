#!/usr/bin/python
# coding: utf-8

# (c) 2021, Famedly GmbH
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
author: "Jadyn Emma Jäger (@jadyn.dev)"
module: synapse_ratelimit
short_description: Change a users rate-limits
description:
    - Change a users rate-limits
options:
    hs_url:
        description:
            - URL of the homeserver, where the CS-API is reachable
        required: true
    access_token:
        description:
            - Shared secret to authenticate registration request
        required: true
    user_id:
        description:
            - The fully qualified MXID of a __local__ user
        required: true
    action:
        description:
            - Which (http) operation should be executed
        required: True
        type: str
        choices: 'get', 'set', 'delete'
        default: 'get'
    messages_per_second:
        description:
            - Set the maximum messages per second (0 = disabled)
        required: False
        type: int
        default: 0
    burst_count:
        description:
            - Set the maximum message burst (0 = disabled)
        required: False
        type: int
        default: 0
requirements: []
'''

EXAMPLES = '''
- name: Disable ratelimits
  synapse_ratelimit:
    hs_url: "https://matrix.org"
    access_token: "long secret string"
    user_id: "@userID:matrix.org"
    action: 'set'
    messages_per_second: 0
    burst_count: 0
'''

RETURN = '''
ratelimit:
 - burst_count: 5
 - messages_per_second: 10
if a ratelimit is set, otherwise `ratelimit` is empty
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.famedly.matrix.plugins.module_utils.synapse import *


def main():
    module_args = dict(
        hs_url=dict(type='str', required=True),
        access_token=dict(type='str', required=True, no_log=True),
        user_id=dict(type='str', required=True),
        action=dict(required=False, type='str', choices=['get', 'set', 'delete'], default='get'),
        messages_per_second=dict(required=False, type='int', default=0),
        burst_count=dict(required=False, type='int', default=0),
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if module.check_mode:
        return result

    action = module.params['action'].lower()
    synapse = AdminApi(home_server=module.params['hs_url'], access_token=module.params['access_token'])
    try:
        ratelimit = synapse.ratelimit.get(module.params['user_id'])
        if action == 'get':
            result['ratelimit'] = ratelimit
            module.exit_json(**result)
        if action == 'set':
            result['ratelimit'] = synapse.ratelimit.set(module.params['user_id'],
                                                        messages_per_second=module.params['messages_per_second'],
                                                        burst_count=module.params['burst_count'])
            result['changed'] = ratelimit != result['ratelimit']
            module.exit_json(**result)
        if action == 'delete':
            result['ratelimit'] = synapse.ratelimit.delete(module.params['user_id'])
            result['changed'] = ratelimit != result['ratelimit']
            module.exit_json(**result)
        raise NotImplementedError("action {} is not implemented".format(action))
    except (Exceptions.HTTPException, Exceptions.MatrixException) as e:
        result['msg'] = str(e)
        module.fail_json(**result)


if __name__ == '__main__':
    main()
