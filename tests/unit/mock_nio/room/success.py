from __future__ import annotations

from copy import deepcopy
from typing import Union, Optional, Sequence, Dict, Any

from nio import (
    RoomBanError,
    RoomBanResponse,
    RoomCreateResponse,
    RoomCreateError,
    RoomGetStateResponse,
    RoomGetStateError,
    RoomInviteResponse,
    RoomInviteError,
    JoinResponse,
    JoinError,
    JoinedRoomsResponse,
    JoinedRoomsError,
    RoomKickResponse,
    RoomKickError,
    RoomResolveAliasError,
    RoomResolveAliasResponse,
    RoomSendResponse,
    RoomSendError,
    RoomUnbanResponse,
    RoomUnbanError,
    RoomGetStateEventResponse,
    RoomGetStateEventError,
    RoomPutStateResponse,
    RoomPutStateError,
)
from nio.api import RoomVisibility, RoomPreset

from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.RoomSimulator import (
    RoomEvents,
)


class RoomBan:
    async def room_ban(
        self, room_id: str, user_id: str, reason: Optional[str] = None
    ) -> Union[RoomBanResponse, RoomBanError]:
        self.room_sim.m_room_member(
            room_id=room_id, membership="ban", sender=self.user, state_key=user_id
        )
        return RoomBanResponse()


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
        return RoomCreateResponse(room_id)


class RoomGetState:
    async def room_get_state(
        self, room_id: str
    ) -> Union[RoomGetStateResponse, RoomGetStateError]:
        return RoomGetStateResponse(
            events=self.room_sim.get_events(room_id), room_id=room_id
        )


class RoomPutState:
    async def room_put_state(
        self,
        room_id: str,
        event_type: str,
        content: Dict[Any, Any],
        state_key: str = "",
    ) -> Union[RoomPutStateResponse, RoomPutStateError]:
        data = deepcopy(RoomEvents.M_ROOM_DUMMY)
        data["content"] = content
        data["type"] = event_type
        data["state_key"] = state_key
        event = self.room_sim.send_event(room_id=room_id, event=data)
        return RoomPutStateResponse(event_id=event["event_id"], room_id=room_id)


class RoomGetStateEvent:
    async def room_get_state_event(
        self, room_id: str, event_type: str, state_key: str = ""
    ) -> Union[RoomGetStateEventResponse, RoomGetStateEventError]:
        event = self.room_sim.get_state_event(room_id, event_type, state_key)
        if event is None:
            return RoomGetStateEventError(room_id=room_id, message="event not found!")
        return RoomGetStateEventResponse(
            content=event["content"],
            event_type=event_type,
            state_key=state_key,
            room_id=room_id,
        )


class RoomInvite:
    async def room_invite(
        self, room_id: str, user_id: str
    ) -> Union[RoomInviteResponse, RoomInviteError]:
        self.room_sim.m_room_member(
            room_id=room_id, membership="join", sender=self.user, state_key=user_id
        )
        return RoomInviteResponse()


class RoomJoin:
    async def join(self, room_id: str) -> Union[JoinResponse, JoinError]:
        self.client_sim.join(room_id)
        return JoinResponse(room_id)


class RoomJoinedRooms:
    async def joined_rooms(self) -> Union[JoinedRoomsResponse, JoinedRoomsError]:
        return JoinedRoomsResponse(self.client_sim.get_joined_rooms())


class RoomKick:
    async def room_kick(
        self, room_id: str, user_id: str, reason: Optional[str] = None
    ) -> Union[RoomKickResponse, RoomKickError]:
        self.room_sim.m_room_member(
            room_id=room_id, membership="leave", sender=self.user, state_key=user_id
        )
        return RoomKickResponse()


class RoomResolveAlias:
    async def room_resolve_alias(
        self, room_alias: str
    ) -> Union[RoomResolveAliasResponse, RoomResolveAliasError]:
        room_id = self.room_sim.resolve_alias(room_alias)
        if room_id is not None:
            return RoomResolveAliasResponse(
                room_id=room_id, room_alias=room_alias, servers=[]
            )
        else:
            return RoomResolveAliasError(message="Room not found!")


class RoomSend:
    async def room_send(
        self,
        room_id: str,
        message_type: str,
        content: Dict[Any, Any],
        tx_id: Optional[str] = None,
        ignore_unverified_devices: bool = False,
    ) -> Union[RoomSendResponse, RoomSendError]:
        return RoomSendResponse(room_id=room_id, event_id="asdf")


class RoomUnban:
    async def room_unban(
        self, room_id: str, user_id: str
    ) -> Union[RoomUnbanResponse, RoomUnbanError]:
        self.room_sim.m_room_member(
            room_id=room_id, membership="leave", sender=self.user, state_key=user_id
        )
        return RoomUnbanResponse()
