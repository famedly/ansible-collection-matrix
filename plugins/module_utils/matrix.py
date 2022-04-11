#!/usr/bin/python
# coding: utf-8

# (c) 2021-2022, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from ansible.module_utils.basic import AnsibleModule, missing_required_lib
import traceback
import asyncio

#Check if all required libs can loded
LIB_IMP_ERR = None
try:
   from nio import *
   HAS_LIB = True
except ImportError:
   LIB_IMP_ERR = traceback.format_exc()
   HAS_LIB = False

class AnsibleNioModule():
    def __init__(self, 
                 custom_spec={},
                 bypass_checks=False,
                 no_log=False,
                 mutually_exclusive=[['password', 'token']],
                 required_together=None,
                 required_one_of=[['password', 'token', 'key']],
                 required_by={'password': 'user_id', 'key': 'user_id'},
                 add_file_common_args=False,
                 supports_check_mode=True,
                 required_if=None,
                 user_logout=True):

        #If a user/password login is provided, should we logout when exiting?
        self.user_logout=user_logout
        
        #Create the Ansible module
        self.module = AnsibleModule(
            argument_spec = AnsibleNioModule.__common_argument_spec(custom_spec),
            bypass_checks=bypass_checks,
            no_log=no_log,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            add_file_common_args=add_file_common_args,
            supports_check_mode = supports_check_mode,
            required_if=required_if,
            required_by=required_by
        )
        
        #Make some values from the module easly accessible
        self.check_mode = self.module.check_mode
        self.params     = self.module.params

        #Fail when matix-nio is not installed
        #WARNING: We don't perform a version check!
        if not HAS_LIB:
            self.module.fail_json(msg=missing_required_lib("matrix-nio"))

    async def matrix_login(self):
        #Login with token or supplied user account
        if self.module.params['token'] is None:
            self.client = AsyncClient(self.module.params['hs_url'], self.module.params['user_id'])
            login_response = await self.client.login(self.module.params['password'])
            if isinstance(login_response, LoginResponse):
                self.access_token     = login_response.access_token
                self.device_id = login_response.device_id
            else:
                result['msg'] = login_response.message
                result['http_status_code'] = login_response.status_code
                module.fail_json(**result)
        else:
            self.client = AsyncClient(self.module.params['hs_url'])
            self.client.access_token = self.module.params['token']

    async def matrix_logout(self):
        if self.client.logged_in:
            await self.client.logout()

    async def exit_json(self, **result):
        if self.module.params['token'] is None and self.user_logout == True:
            await self.matrix_logout()
        await self.client.close()
        self.module.exit_json(**result)

    async def fail_json(self, **result):
        if self.module.params['token'] is None and self.user_logout == True:
            await self.matrix_logout()
        await self.client.close()
        self.module.fail_json(**result)

    @staticmethod
    def __common_argument_spec(custom_spec: dict):
        argument_spec = dict(
            hs_url=dict(type='str', required=True),
            user_id=dict(type='str', required=False),
            password=dict(type='str', required=False, no_log=True),
            token=dict(type='str', required=False, no_log=True)
        )
        return {**argument_spec, **custom_spec}

