#!/usr/bin/python
# Copyright: (c) 2018
# Apache 2.0
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = '''
---
author: "Emmanouil Kampitakis (@madonius)"
module: matrix_signing_key
short_description: Create a signing key file if not exists
description:
    - Create a signing key file if not exists
options:
    path:
        description:
            - Path to the signing key file
        required: true
        type: str
requirements:
    -  signedjson (Python library)
'''

EXAMPLES = '''
- name: Create signing key file
  matrix_signing_key:
    changed: "/path/to/file"
'''

RETURN = '''
'''

import os
import traceback

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

# Check if all required libs can load
LIB_IMP_ERR = None
try:
    from signedjson import key
    HAS_LIB = True
except ImportError:
    LIB_IMP_ERR = traceback.format_exc()
    HAS_LIB = False


def write_signing_key(path):
    with open(path, 'w') as file:
        key.write_signing_keys(
            file,
            [key.generate_signing_key('first')]
        )


def run_module():
    module_args = dict(
        path=dict(type='str', required=True),
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    if not HAS_LIB:
        module.fail_json(msg=missing_required_lib("signedjson"))

    signing_key_path = module.params['path']

    signing_key_exists = os.path.isfile(signing_key_path)

    if not signing_key_exists:
        result['changed'] = True
        if module.check_mode:
            module.exit_json(**result)
        try:
            write_signing_key(signing_key_path)
        except OSError as e:
            module.fail_json(msg=str(e))

    module.exit_json(**result)


def main():
    run_module()


if __name__ == '__main__':
    main()
