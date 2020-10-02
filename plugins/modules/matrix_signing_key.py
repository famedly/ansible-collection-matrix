#!/bin/python3
# Copyright: (c) 2018, Emmanouil Kampitakis <info@kampitakis.de>
# Apache 2.0

import os
from ansible.module_utils.basic import AnsibleModule
from signedjson import key

def write_signing_key(path):
    with open(path,'w') as file:
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

    signing_key_path = module.params['path']

    signing_key_exists = os.path.isfile(signing_key_path)

    if not signing_key_exists:
        result['changed'] = True
        if module.check_mode:
            module.exit_json(**result)
        write_signing_key(signing_key_path)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
