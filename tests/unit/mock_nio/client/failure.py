from __future__ import annotations
from typing import Optional, Union
from nio import LoginResponse, LoginError, LogoutResponse, LogoutError


class ClientLogin:
    async def login(self,
                    password: Optional[str] = None,
                    device_name: Optional[str] = "",
                    token: Optional[str] = None) -> Union[LoginResponse, LoginError]:
        return LoginError(message="Mocked failure")


class ClientLogout:
    async def logout(self,
                     all_devices: bool = False) -> Union[LogoutResponse, LogoutError]:
        return LogoutError(message="Mocked failure")
