from __future__ import annotations

import abc
import os
from typing import Union, Optional, Dict, Any, Sequence

from nio import AsyncClientConfig, \
    LoginResponse, LoginError, \
    LogoutResponse, LogoutError, \
    RoomGetStateResponse, RoomGetStateError, \
    RoomBanResponse, RoomBanError, \
    RoomUnbanResponse, RoomUnbanError, \
    RoomKickResponse, RoomKickError, \
    RoomInviteResponse, RoomInviteError, \
    RoomSendResponse, RoomSendError, \
    RoomResolveAliasResponse, RoomResolveAliasError, \
    JoinedRoomsResponse, JoinedRoomsError, \
    JoinResponse, JoinError, \
    RoomCreateResponse, RoomCreateError, \
    RoomGetStateEventResponse, RoomGetStateEventError, \
    RoomPutStateResponse, RoomPutStateError
from nio.api import RoomVisibility, RoomPreset

from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.ClientSimulator import ClientSimulator
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.RoomSimulator import RoomSimulator


class MatrixNioBase(metaclass=abc.ABCMeta):
    ACCESS_TOKEN: str = 'supersecrettoken'

    def __init__(self,
                 homeserver: str,
                 user: str = "",
                 device_id: Optional[str] = "",
                 store_path: Optional[str] = "",
                 config: Optional[AsyncClientConfig] = None,
                 ssl: Optional[bool] = None,
                 proxy: Optional[str] = None):
        self.homeserver = homeserver
        self.user = user
        self.device_id = device_id
        self.store_path = store_path
        self.config = config
        self.ssl = ssl
        self.proxy = proxy
        self.room_sim = RoomSimulator(os.getenv("ROOM_SIMULATOR"))
        self.client_sim = ClientSimulator(os.getenv("CLIENT_SIMULATOR"))
        self.logged_in = False

    @abc.abstractmethod
    async def login(self,
                    password: Optional[str] = None,
                    device_name: Optional[str] = "",
                    token: Optional[str] = None) -> Union[LoginResponse, LoginError]:
        pass

    @abc.abstractmethod
    async def logout(self,
                     all_devices: bool = False) -> Union[LogoutResponse, LogoutError]:
        pass

    async def close(self):
        pass

    @abc.abstractmethod
    async def room_get_state(self,
                             room_id: str) -> Union[RoomGetStateResponse, RoomGetStateError]:
        pass

    @abc.abstractmethod
    async def room_put_state(self,
                             room_id: str,
                             event_type: str,
                             content: Dict[Any, Any],
                             state_key: str = "") -> Union[RoomPutStateResponse, RoomPutStateError]:
        pass

    @abc.abstractmethod
    async def room_get_state_event(self,
                                   room_id: str,
                                   event_type: str,
                                   state_key: str = "") -> Union[RoomGetStateEventResponse, RoomGetStateEventError]:
        pass

    @abc.abstractmethod
    async def room_ban(self,
                       room_id: str,
                       user_id: str,
                       reason: Optional[str] = None) -> Union[RoomBanResponse, RoomBanError]:
        pass

    @abc.abstractmethod
    async def room_unban(self,
                         room_id: str,
                         user_id: str) -> Union[RoomUnbanResponse, RoomUnbanError]:
        pass

    @abc.abstractmethod
    async def room_kick(self,
                        room_id: str,
                        user_id: str,
                        reason: Optional[str] = None) -> Union[RoomKickResponse, RoomKickError]:
        pass

    @abc.abstractmethod
    async def room_invite(self,
                          room_id: str,
                          user_id: str) -> Union[RoomInviteResponse, RoomInviteError]:
        pass

    @abc.abstractmethod
    async def room_send(self,
                        room_id: str,
                        message_type: str,
                        content: Dict[Any, Any],
                        tx_id: Optional[str] = None,
                        ignore_unverified_devices: bool = False) -> Union[RoomSendResponse, RoomSendError]:
        pass

    @abc.abstractmethod
    async def room_resolve_alias(self,
                                 room_alias: str) -> Union[RoomResolveAliasResponse, RoomResolveAliasError]:
        pass

    @abc.abstractmethod
    async def joined_rooms(self) -> Union[JoinedRoomsResponse, JoinedRoomsError]:
        pass

    @abc.abstractmethod
    async def join(self, room_id: str) -> Union[JoinResponse, JoinError]:
        pass

    @abc.abstractmethod
    async def room_create(self,
                          visibility: RoomVisibility = RoomVisibility.private,
                          alias: Optional[str] = None,
                          name: Optional[str] = None,
                          topic: Optional[str] = None,
                          room_version: Optional[str] = None,
                          federate: bool = True,
                          is_direct: bool = False,
                          preset: Optional[RoomPreset] = None,
                          invite: Sequence[str] = (),
                          initial_state: Sequence[Dict[str, Any]] = (),
                          power_level_override: Optional[Dict[str, Any]] = None,
                          predecessor: Optional[Dict[str, Any]] = None,
                          space: bool = False,
                          ) -> Union[RoomCreateResponse, RoomCreateError]:
        pass
