from __future__ import annotations

import abc

from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import failure


class RoomFailure(
    failure.RoomBan,
    failure.RoomCreate,
    failure.RoomGetState,
    failure.RoomPutState,
    failure.RoomGetStateEvent,
    failure.RoomInvite,
    failure.RoomJoin,
    failure.RoomKick,
    failure.RoomSend,
    failure.RoomUnban,
    failure.RoomJoinedRooms,
    failure.RoomResolveAlias,
    abc.ABC,
):
    pass
