from __future__ import (absolute_import, division, print_function, annotations)

import types

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_member

from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import MatrixNioBase
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioSuccess import MatrixNioSuccess
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.RoomSimulator import RoomSimulator
from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import failure

from ansible_collections.famedly.matrix.tests.unit.utils import AnsibleExitJson, AnsibleFailJson, assert_expression, \
    set_module_args, exit_json, fail_json


class TestAnsibleModuleMatrixMember:
    @staticmethod
    def patchAnsibleNioModule(monkeypatch: MonkeyPatch, mock_class: type(MatrixNioBase)):
        # Mock ansible functions
        monkeypatch.setattr(matrix.AnsibleModule, 'exit_json', exit_json)
        monkeypatch.setattr(matrix.AnsibleModule, 'fail_json', fail_json)
        # Mock MatrixNio
        for method in MatrixNioBase.__dict__:
            if isinstance(getattr(mock_class, method), (types.FunctionType, types.BuiltinFunctionType)):
                monkeypatch.setattr(matrix.AsyncClient, method, getattr(mock_class, method))
        monkeypatch.setattr(matrix.AsyncClient, 'logged_in', False)
        # Setup RoomSimulator
        simulator = RoomSimulator()
        simulator.add_room('!myroomid:matrix.example.tld')
        simulator.m_room_create('!myroomid:matrix.example.tld', '@admin:example.tld')
        simulator.m_room_member(room_id='!myroomid:matrix.example.tld', membership="join", sender='@myuser:matrix.example.tld',
                                state_key='@user1:matrix.example.tld')
        simulator.m_room_member(room_id='!myroomid:matrix.example.tld', membership="join", sender='@myuser:matrix.example.tld',
                                state_key='@user2:matrix.example.tld')
        simulator.m_room_member(room_id='!myroomid:matrix.example.tld', membership="ban", sender='@myuser:matrix.example.tld',
                                state_key='@user0:matrix.example.tld')
        monkeypatch.setenv('ROOM_SIMULATOR', simulator.export())

    def test_no_changes(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'user_ids': ['@user1:matrix.example.tld', '@user2:matrix.example.tld']
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is False)
        assert_expression(ansible_result['banned'] == [])
        assert_expression(ansible_result['unbanned'] == [])
        assert_expression(ansible_result['kicked'] == [])
        assert_expression(ansible_result['invited'] == [])
        assert_expression(list(ansible_result['members']) == ['@user1:matrix.example.tld', '@user2:matrix.example.tld'])

    def test_add_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'user_ids': ['@user1:matrix.example.tld', '@user2:matrix.example.tld', '@user3:matrix.example.tld']
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(ansible_result['banned'] == [])
        assert_expression(ansible_result['unbanned'] == [])
        assert_expression(ansible_result['kicked'] == [])
        assert_expression(ansible_result['invited'] == ['@user3:matrix.example.tld'])
        assert_expression(list(ansible_result['members']) == ['@user1:matrix.example.tld', '@user2:matrix.example.tld',
                                                              '@user3:matrix.example.tld'])

    def test_kick_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'kicked',
            'user_ids': ['@user1:matrix.example.tld']
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(ansible_result['banned'] == [])
        assert_expression(ansible_result['unbanned'] == [])
        assert_expression(ansible_result['kicked'] == ['@user1:matrix.example.tld'])
        assert_expression(ansible_result['invited'] == [])
        assert_expression(list(ansible_result['members']) == ['@user2:matrix.example.tld'])

    def test_ban_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'banned',
            'user_ids': ['@user1:matrix.example.tld']
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(ansible_result['banned'] == ['@user1:matrix.example.tld'])
        assert_expression(ansible_result['unbanned'] == [])
        assert_expression(ansible_result['kicked'] == [])
        assert_expression(ansible_result['invited'] == [])
        assert_expression(list(ansible_result['members']) == ['@user2:matrix.example.tld'])

    def test_unban_user(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'user_ids': ['@user0:matrix.example.tld']
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(ansible_result['banned'] == [])
        assert_expression(ansible_result['unbanned'] == ['@user0:matrix.example.tld'])
        assert_expression(ansible_result['kicked'] == [])
        assert_expression(ansible_result['invited'] == ['@user0:matrix.example.tld'])
        assert_expression(list(ansible_result['members']) == ['@user1:matrix.example.tld', '@user2:matrix.example.tld',
                                                              '@user0:matrix.example.tld'])

    def test_exclusive(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'exclusive': True,
            'user_ids': ['@user2:matrix.example.tld']
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_member.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(ansible_result['banned'] == [])
        assert_expression(ansible_result['unbanned'] == [])
        assert_expression(ansible_result['kicked'] == ['@user1:matrix.example.tld'])
        assert_expression(ansible_result['invited'] == [])
        assert_expression(list(ansible_result['members']) == ['@user2:matrix.example.tld'])

    def test_add_user_fail(self, monkeypatch):
        class TestClass(failure.RoomInvite, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'user_ids': ['@user1:matrix.example.tld', '@user2:matrix.example.tld', '@user3:matrix.example.tld']
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_kick_user_fail(self, monkeypatch):
        class TestClass(failure.RoomKick, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'kicked',
            'user_ids': ['@user1:matrix.example.tld']
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_ban_user_fail(self, monkeypatch):
        class TestClass(failure.RoomBan, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'banned',
            'user_ids': ['@user1:matrix.example.tld']
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_unban_user_fail(self, monkeypatch):
        class TestClass(failure.RoomUnban, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'user_ids': ['@user0:matrix.example.tld']
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()

    def test_get_state_fail(self, monkeypatch):
        class TestClass(failure.RoomGetState, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'room_id': '!myroomid:matrix.example.tld',
            'state': 'member',
            'user_ids': ['@user0:matrix.example.tld']
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_member.main()
