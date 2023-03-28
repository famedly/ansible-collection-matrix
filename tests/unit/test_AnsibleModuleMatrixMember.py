from __future__ import absolute_import, division, print_function, annotations

import json
import types

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_member

from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import (
    MatrixNioBase,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioSuccess import (
    MatrixNioSuccess,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.RoomSimulator import (
    RoomSimulator,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import failure

from ansible_collections.famedly.matrix.plugins.module_utils import synapse
from ansible_collections.famedly.matrix.tests.unit.mock_synapse.requests.RequestsBase import (
    RequestsBase,
)

from ansible_collections.famedly.matrix.tests.unit.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    assert_expression,
    set_module_args,
    exit_json,
    fail_json,
)


class TestAnsibleModuleMatrixMember:
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
        simulator = RoomSimulator()
        simulator.add_room("!myroomid:matrix.example.tld")
        simulator.m_room_create("!myroomid:matrix.example.tld", "@admin:example.tld")
        simulator.m_room_member(
            room_id="!myroomid:matrix.example.tld",
            membership="join",
            sender="@myuser:matrix.example.tld",
            state_key="@user1:matrix.example.tld",
        )
        simulator.m_room_member(
            room_id="!myroomid:matrix.example.tld",
            membership="join",
            sender="@myuser:matrix.example.tld",
            state_key="@user2:matrix.example.tld",
        )
        simulator.m_room_member(
            room_id="!myroomid:matrix.example.tld",
            membership="ban",
            sender="@myuser:matrix.example.tld",
            state_key="@user0:matrix.example.tld",
        )
        monkeypatch.setenv("ROOM_SIMULATOR", simulator.export())

    @staticmethod
    def patchAdminApiModule(
        monkeypatch: MonkeyPatch, target_module, mock_class: type(RequestsBase)
    ):
        # Mock Admin API
        for method in RequestsBase.__dict__:
            if isinstance(
                getattr(mock_class, method),
                (types.FunctionType, types.BuiltinFunctionType),
            ):
                monkeypatch.setattr(
                    synapse.requests, method, getattr(mock_class, method)
                )

    def test_check_mode(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": ["@user1:matrix.example.tld", "@user2:matrix.example.tld"],
            },
            check_mode=True,
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == [])
        assert_expression(ansible_result["invited"] == [])
        assert_expression(
            list(ansible_result["members"])
            == ["@user1:matrix.example.tld", "@user2:matrix.example.tld"]
        )

    def test_no_changes(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": ["@user1:matrix.example.tld", "@user2:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is False)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == [])
        assert_expression(ansible_result["invited"] == [])
        assert_expression(
            list(ansible_result["members"])
            == ["@user1:matrix.example.tld", "@user2:matrix.example.tld"]
        )

    def test_add_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": [
                    "@user1:matrix.example.tld",
                    "@user2:matrix.example.tld",
                    "@user3:matrix.example.tld",
                ],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == [])
        assert_expression(ansible_result["invited"] == ["@user3:matrix.example.tld"])
        assert_expression(
            list(ansible_result["members"])
            == [
                "@user1:matrix.example.tld",
                "@user2:matrix.example.tld",
                "@user3:matrix.example.tld",
            ]
        )

    def test_kick_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "kicked",
                "user_ids": ["@user1:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == ["@user1:matrix.example.tld"])
        assert_expression(ansible_result["invited"] == [])
        assert_expression(
            list(ansible_result["members"]) == ["@user2:matrix.example.tld"]
        )

    def test_ban_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "banned",
                "user_ids": ["@user1:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == ["@user1:matrix.example.tld"])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == [])
        assert_expression(ansible_result["invited"] == [])
        assert_expression(
            list(ansible_result["members"]) == ["@user2:matrix.example.tld"]
        )

    def test_unban_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": ["@user0:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == ["@user0:matrix.example.tld"])
        assert_expression(ansible_result["kicked"] == [])
        assert_expression(ansible_result["invited"] == ["@user0:matrix.example.tld"])
        assert_expression(
            list(ansible_result["members"])
            == [
                "@user1:matrix.example.tld",
                "@user2:matrix.example.tld",
                "@user0:matrix.example.tld",
            ]
        )

    def test_exclusive(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "exclusive": True,
                "user_ids": ["@user2:matrix.example.tld", "@user3:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == ["@user1:matrix.example.tld"])
        assert_expression(ansible_result["invited"] == ["@user3:matrix.example.tld"])
        assert_expression(
            list(ansible_result["members"])
            == ["@user2:matrix.example.tld", "@user3:matrix.example.tld"]
        )

    def test_force_join(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        self.patchAdminApiModule(monkeypatch, matrix_member, RequestsBase)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": "supersecrettoken",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "force_join": True,
                "user_ids": ["@user3:matrix.example.tld"],
            }
        )
        response = {
            "_synapse/admin/v1/join/%21myroomid%3Amatrix.example.tld": {
                "status": 200,
                "content": '{"room_id": "!myroomid:matrix.example.tld"}',
            }
        }
        monkeypatch.setenv("REQUESTS_POST_RESPONSE", json.dumps(response))
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        print(ansible_result)
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(ansible_result["kicked"] == [])
        assert_expression(ansible_result["invited"] == [])
        assert_expression(ansible_result["joined"] == ["@user3:matrix.example.tld"])
        # TODO: make this assertion work. Needs proper mocking of Admin API that
        #       calls the mocked nio in order to have the members changed
        # assert_expression(
        #     list(ansible_result["members"])
        #     == [
        #         "@user1:matrix.example.tld",
        #         "@user2:matrix.example.tld",
        #         "@user3:matrix.example.tld",
        #     ]
        # )

    def test_exclusive_force_join(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        self.patchAdminApiModule(monkeypatch, matrix_member, RequestsBase)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": "supersecrettoken",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "force_join": True,
                "exclusive": True,
                "user_ids": ["@user3:matrix.example.tld"],
            }
        )
        response = {
            "_synapse/admin/v1/join/%21myroomid%3Amatrix.example.tld": {
                "status": 200,
                "content": '{"room_id": "!myroomid:matrix.example.tld"}',
            }
        }
        monkeypatch.setenv("REQUESTS_POST_RESPONSE", json.dumps(response))
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        print(ansible_result)
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["banned"] == [])
        assert_expression(ansible_result["unbanned"] == [])
        assert_expression(
            ansible_result["kicked"]
            == ["@user1:matrix.example.tld", "@user2:matrix.example.tld"]
        )
        assert_expression(ansible_result["invited"] == [])
        assert_expression(ansible_result["joined"] == ["@user3:matrix.example.tld"])
        # TODO: make this assertion work. Needs proper mocking of Admin API that
        #       calls the mocked nio in order to have the members changed
        # assert_expression(
        #     list(ansible_result["members"])
        #     == [
        #         "@user3:matrix.example.tld",
        #     ]
        # )

    def test_exclusive_kick_fail(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": "supersecrettoken",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "kicked",
                "user_ids": ["@user1:matrix.example.tld"],
                "exclusive": True,
            },
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()
        assert_expression(
            "exclusive=True can only be used with state=member"
            in result.value.result["msg"]
        )

    def test_force_join_kick_fail(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": "supersecrettoken",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "kicked",
                "user_ids": ["@user1:matrix.example.tld"],
                "force_join": True,
            },
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()
        assert_expression(
            "force_join=True can only be used with state=member"
            in result.value.result["msg"]
        )

    def test_add_user_fail(self, monkeypatch):
        class TestClass(failure.RoomInvite, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": [
                    "@user1:matrix.example.tld",
                    "@user2:matrix.example.tld",
                    "@user3:matrix.example.tld",
                ],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_kick_user_fail(self, monkeypatch):
        class TestClass(failure.RoomKick, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "kicked",
                "user_ids": ["@user1:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_ban_user_fail(self, monkeypatch):
        class TestClass(failure.RoomBan, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "banned",
                "user_ids": ["@user1:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_unban_user_fail(self, monkeypatch):
        class TestClass(failure.RoomUnban, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": ["@user0:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_get_state_fail(self, monkeypatch):
        class TestClass(failure.RoomGetState, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "user_ids": ["@user0:matrix.example.tld"],
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_force_join_fail_privileges(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        self.patchAdminApiModule(monkeypatch, matrix_member, RequestsBase)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": "notaserveradmintoken",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "force_join": True,
                "user_ids": ["@user3:matrix.example.tld"],
            }
        )
        response = {
            "_synapse/admin/v1/join/%21myroomid%3Amatrix.example.tld": {
                "status": 403,
                "content": '{"errcode": "M_FORBIDDEN", "error": "You are not a server admin"}',
            }
        }
        monkeypatch.setenv("REQUESTS_POST_RESPONSE", json.dumps(response))
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()
        print(result.value.result["msg"])
        assert_expression("M_FORBIDDEN" in result.value.result["msg"])

    def test_exclusive_force_join_fail_privileges(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        self.patchAdminApiModule(monkeypatch, matrix_member, RequestsBase)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": "notaserveradmintoken",
                "room_id": "!myroomid:matrix.example.tld",
                "state": "member",
                "force_join": True,
                "exclusive": True,
                "user_ids": ["@user3:matrix.example.tld"],
            }
        )
        response = {
            "_synapse/admin/v1/join/%21myroomid%3Amatrix.example.tld": {
                "status": 403,
                "content": '{"errcode": "M_FORBIDDEN", "error": "You are not a server admin"}',
            }
        }
        monkeypatch.setenv("REQUESTS_POST_RESPONSE", json.dumps(response))
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()
        print(result.value.result["msg"])
        assert_expression("M_FORBIDDEN" in result.value.result["msg"])
