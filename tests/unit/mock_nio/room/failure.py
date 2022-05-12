from __future__ import annotations

from typing import Union, Optional, Sequence, Dict, Any

from nio import RoomBanError, RoomBanResponse, \
    RoomCreateResponse, RoomCreateError, \
    RoomGetStateResponse, RoomGetStateError, \
    RoomInviteResponse, RoomInviteError, \
    JoinResponse, JoinError, \
    JoinedRoomsResponse, JoinedRoomsError, \
    RoomKickResponse, RoomKickError, \
    RoomResolveAliasError, RoomResolveAliasResponse, \
    RoomSendResponse, RoomSendError, \
    RoomUnbanResponse, RoomUnbanError, \
    RoomGetStateEventResponse, RoomGetStateEventError, \
    RoomPutStateResponse, RoomPutStateError
from nio.api import RoomVisibility, RoomPreset


class RoomBan:
    async def room_ban(self,
                       room_id: str,
                       user_id: str,
                       reason: Optional[str] = None) -> Union[RoomBanResponse, RoomBanError]:
        return RoomBanError(message="Mocked failure")


class RoomCreate:
    async def room_create(
            self,
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
        room_id = self.room_sim.create_room(alias=alias)
        return RoomCreateError(message="Mocked failure")


class RoomGetState:
    async def room_get_state(self,
                             room_id: str) -> Union[RoomGetStateResponse, RoomGetStateError]:
        return RoomGetStateError(message="Mocked failure")


class RoomPutState:
    async def room_put_state(self,
                             room_id: str,
                             event_type: str,
                             content: Dict[Any, Any],
                             state_key: str = "") -> Union[RoomPutStateResponse, RoomPutStateError]:
        return RoomPutStateError(room_id=room_id, message="Mocked failure")


class RoomGetStateEvent:
    async def room_get_state_event(self,
                                   room_id: str,
                                   event_type: str,
                                   state_key: str = "") -> Union[RoomGetStateEventResponse, RoomGetStateEventError]:
        return RoomGetStateEventError(room_id=room_id, message="Mocked failure")


class RoomInvite:
    async def room_invite(self,
                          room_id: str,
                          user_id: str) -> Union[RoomInviteResponse, RoomInviteError]:
        return RoomInviteError(message="Mocked failure")


class RoomJoin:
    async def join(self, room_id: str) -> Union[JoinResponse, JoinError]:
        self.client_sim.join(room_id)
        return JoinError(message="Mocked failure")


class RoomJoinedRooms:
    async def joined_rooms(self) -> Union[JoinedRoomsResponse, JoinedRoomsError]:
        return JoinedRoomsError(message="Mocked failure")


class RoomKick:
    async def room_kick(self,
                        room_id: str,
                        user_id: str,
                        reason: Optional[str] = None) -> Union[RoomKickResponse, RoomKickError]:
        return RoomKickError(message="Mocked failure")


class RoomResolveAlias:
    async def room_resolve_alias(self,
                                 room_alias: str) -> Union[RoomResolveAliasResponse, RoomResolveAliasError]:
        return RoomResolveAliasError(message="Mocked failure")


class RoomSend:
    async def room_send(self,
                        room_id: str,
                        message_type: str,
                        content: Dict[Any, Any],
                        tx_id: Optional[str] = None,
                        ignore_unverified_devices: bool = False) -> Union[RoomSendResponse, RoomSendError]:
        return RoomSendError(room_id=room_id, message="Mocked failure")


class RoomUnban:
    async def room_unban(self,
                         room_id: str,
                         user_id: str) -> Union[RoomUnbanResponse, RoomUnbanError]:
        return RoomUnbanError(message="Mocked failure")
