from __future__ import annotations
from typing import Optional, Union
from nio import LoginResponse, LoginError, LogoutResponse, LogoutError
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import MatrixNioBase


class ClientLogin:
    async def login(self,
                    password: Optional[str] = None,
                    device_name: Optional[str] = "",
                    token: Optional[str] = None) -> Union[LoginResponse, LoginError]:
        self.logged_in = True
        self.access_token = MatrixNioBase.ACCESS_TOKEN
        return LoginResponse(user_id=self.user, device_id=self.device_id, access_token=self.access_token)


class ClientLogout:
    async def logout(self,
                     all_devices: bool = False) -> Union[LogoutResponse, LogoutError]:
        self.logged_in = False
        self.access_token = None
        return LogoutResponse()
