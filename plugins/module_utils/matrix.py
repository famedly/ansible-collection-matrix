# coding: utf-8

# (c) 2021-2022, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import absolute_import, division, print_function

__metaclass__ = type

import traceback
from typing import Union

from ansible.module_utils.basic import AnsibleModule, missing_required_lib

# Check if all required libs can load
LIB_IMP_ERR = None
try:
    from nio import (
        AsyncClient,
        AsyncClientConfig,
        Api,
        LoginResponse,
        LoginError,
        LogoutResponse,
        LogoutError,
        RoomGetStateResponse,
        RoomGetStateError,
        RoomBanResponse,
        RoomBanError,
        RoomUnbanResponse,
        RoomUnbanError,
        RoomKickResponse,
        RoomKickError,
        RoomInviteResponse,
        RoomInviteError,
        RoomResolveAliasResponse,
        RoomResolveAliasError,
        JoinedRoomsResponse,
        JoinedRoomsError,
    )

    HAS_LIB = True
except ImportError:
    LIB_IMP_ERR = traceback.format_exc()
    HAS_LIB = False


class AnsibleNioModule:
    def __init__(
        self,
        custom_spec=None,
        bypass_checks=False,
        no_log=False,
        mutually_exclusive=None,
        required_together=None,
        required_one_of=None,
        required_by=None,
        add_file_common_args=False,
        supports_check_mode=True,
        required_if=None,
        user_logout=None,
        add_default_arguments=True,
    ):
        if add_default_arguments:
            if required_by is None:
                required_by = {"password": "user_id"}

            if required_one_of is None:
                required_one_of = [["password", "token"]]

            if mutually_exclusive is None:
                mutually_exclusive = [["password", "token"]]

            if custom_spec is None:
                custom_spec = {}

            custom_spec = AnsibleNioModule.__common_argument_spec(custom_spec)
        else:
            if required_by is None:
                required_by = {}

            if required_one_of is None:
                required_one_of = []

            if mutually_exclusive is None:
                mutually_exclusive = []

            if custom_spec is None:
                custom_spec = {}

        # Create the Ansible module
        self.module = AnsibleModule(
            argument_spec=custom_spec,
            bypass_checks=bypass_checks,
            no_log=no_log,
            mutually_exclusive=mutually_exclusive,
            required_together=required_together,
            required_one_of=required_one_of,
            add_file_common_args=add_file_common_args,
            supports_check_mode=supports_check_mode,
            required_if=required_if,
            required_by=required_by,
        )

        if user_logout is None:
            # If a user/password login is provided, should we logout when exiting?
            self.user_logout = self.module.params.get("token") is None
        else:
            self.user_logout = user_logout

        # Make some values from the module easly accessible
        self.check_mode = self.module.check_mode
        self.params = self.module.params

        # Fail when matix-nio is not installed
        # WARNING: We don't perform a version check!
        if not HAS_LIB:
            self.module.fail_json(msg=missing_required_lib("matrix-nio"))

    async def matrix_login(self):
        # Login with token or supplied user account
        if self.module.params.get("token") is None:
            self.client = AsyncClient(
                self.module.params.get("hs_url"), self.module.params.get("user_id")
            )
            login_response = await self.client.login(
                password=self.module.params.get("password")
            )
            if not isinstance(login_response, LoginResponse):
                result = {
                    "msg": login_response.message,
                    "http_status_code": login_response.status_code,
                }
                self.module.fail_json(**result)
        else:
            self.client = AsyncClient(self.module.params.get("hs_url"))
            self.client.access_token = self.module.params.get("token")

    @property
    def access_token(self) -> str:
        return self.client.access_token

    @property
    def device_id(self) -> Union[str, None]:
        return self.client.device_id

    async def matrix_logout(self):
        if not self.module.check_mode and self.client.logged_in:
            request = await self.client.logout()
            if isinstance(request, LogoutError):
                result = {"msg": request.message}
                self.module.fail_json(**result)

    async def exit_json(self, **result):
        if self.module.params.get("token") is None and self.user_logout is True:
            await self.matrix_logout()
        if not self.module.check_mode:
            await self.client.close()
        self.module.exit_json(**result)

    async def fail_json(self, **result):
        if self.module.params.get("token") is None and self.user_logout is True:
            await self.matrix_logout()
        if not self.module.check_mode:
            await self.client.close()
        self.module.fail_json(**result)

    @staticmethod
    def __common_argument_spec(custom_spec: dict):
        argument_spec = dict(
            hs_url=dict(type="str", required=True),
            user_id=dict(type="str", required=False),
            password=dict(type="str", required=False, no_log=True),
            token=dict(type="str", required=False, no_log=True),
        )
        return {**argument_spec, **custom_spec}
