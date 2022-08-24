from __future__ import absolute_import, division, print_function, annotations

import types
from copy import deepcopy

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_state
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import (
    MatrixNioBase,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioSuccess import (
    MatrixNioSuccess,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import failure
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.RoomSimulator import (
    RoomSimulator,
    RoomEvents,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.ClientSimulator import (
    ClientSimulator,
)
from ansible_collections.famedly.matrix.tests.unit.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    set_module_args,
    exit_json,
    fail_json,
    assert_expression,
)


class TestAnsibleModuleMatrixState:
    @staticmethod
    def patchAnsibleNioModule(
        monkeypatch: MonkeyPatch, mock_class: type(MatrixNioBase)
    ):
        # Mock ansible functions
        monkeypatch.setattr(matrix.AnsibleModule, "exit_json", exit_json)
        monkeypatch.setattr(matrix.AnsibleModule, "fail_json", fail_json)
        # Mock MatrixNio
        for method in MatrixNioBase.__dict__:
            if isinstance(
                getattr(mock_class, method),
                (types.FunctionType, types.BuiltinFunctionType),
            ):
                monkeypatch.setattr(
                    matrix.AsyncClient, method, getattr(mock_class, method)
                )
        monkeypatch.setattr(matrix.AsyncClient, "logged_in", False)
        # Setup RoomSimulator
        room_simulator = RoomSimulator()
        room_simulator.add_room(
            "!existingroomid:matrix.example.tld", "#existingroom:matrix.example.tld"
        )
        room_simulator.add_room(
            "!otherroomid:matrix.example.tld", "#otherroom:matrix.example.tld"
        )
        dummy_event = deepcopy(RoomEvents.M_ROOM_DUMMY)
        dummy_event["sender"] = "myuser"
        dummy_event["state_key"] = "mystatekey"
        room_simulator.send_event(
            room_id="!existingroomid:matrix.example.tld", event=dummy_event
        )
        room_simulator.send_event(
            room_id="!otherroomid:matrix.example.tld", event=dummy_event
        )
        monkeypatch.setenv("ROOM_SIMULATOR", room_simulator.export())
        # Setup ClientSimulator
        client_simulator = ClientSimulator()
        client_simulator.join("!existingroomid:matrix.example.tld")
        monkeypatch.setenv("CLIENT_SIMULATOR", client_simulator.export())

    # In room; Event already sent
    def test_no_changes(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!existingroomid:matrix.example.tld",
                "event_type": "m.room.dummy",
                "state_key": "mystatekey",
                "content": RoomEvents.M_ROOM_DUMMY["content"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_state.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is False)

    # Not in room; Event already sent
    def test_not_in_room_fail(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!otherroomid:matrix.example.tld",
                "event_type": "m.room.dummy",
                "state_key": "mystatekey",
                "content": RoomEvents.M_ROOM_DUMMY["content"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_state.main()
        ansible_result = result.value.result
        assert_expression(
            ansible_result["msg"] == "Not in the room you're trying to set state for."
        )

    # Not in room; Event already sent
    def test_joined_rooms_fail(self, monkeypatch):
        class TestClass(failure.RoomJoinedRooms, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!otherroomid:matrix.example.tld",
                "event_type": "m.room.dummy",
                "state_key": "mystatekey",
                "content": RoomEvents.M_ROOM_DUMMY["content"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_state.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["msg"] == "Couldn't get joined rooms.")

    # In room; Event not send yet
    def test_send_event(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!existingroomid:matrix.example.tld",
                "event_type": "m.room.dummy",
                "state_key": "myotherstatekey",
                "content": RoomEvents.M_ROOM_DUMMY["content"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_state.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)

    # In room; send Event
    def test_send_event_fail(self, monkeypatch):
        class TestClass(failure.RoomPutState, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!existingroomid:matrix.example.tld",
                "event_type": "m.room.dummy",
                "state_key": "myotherstatekey",
                "content": RoomEvents.M_ROOM_DUMMY["content"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_state.main()
        ansible_result = result.value.result
        assert_expression("Couldn't set state" in ansible_result["msg"])
