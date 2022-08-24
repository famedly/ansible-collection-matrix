from __future__ import annotations

import abc

from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import success


class RoomSuccess(
    success.RoomBan,
    success.RoomCreate,
    success.RoomGetState,
    success.RoomPutState,
    success.RoomGetStateEvent,
    success.RoomInvite,
    success.RoomJoin,
    success.RoomKick,
    success.RoomSend,
    success.RoomUnban,
    success.RoomJoinedRooms,
    success.RoomResolveAlias,
    abc.ABC,
):
    pass
