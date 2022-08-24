from __future__ import annotations

from abc import ABC

from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import (
    MatrixNioBase,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.client.ClientSuccess import (
    ClientSuccess,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.room.RoomSuccess import (
    RoomSuccess,
)


@MatrixNioBase.register
class MatrixNioSuccess(ClientSuccess, RoomSuccess, MatrixNioBase):
    pass
