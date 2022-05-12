from __future__ import (absolute_import, division, print_function, annotations)

import re
import types

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_room


from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import failure
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import MatrixNioBase
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioSuccess import MatrixNioSuccess
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.ClientSimulator import ClientSimulator
from ansible_collections.famedly.matrix.tests.unit.mock_nio.utils.RoomSimulator import RoomSimulator
from ansible_collections.famedly.matrix.tests.unit.utils import AnsibleExitJson, AnsibleFailJson, set_module_args, \
    exit_json, fail_json, assert_expression


class TestAnsibleModuleMatrixRoom:
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
        room_simulator = RoomSimulator()
        room_simulator.add_room('!myroomid:matrix.example.tld', '#myroom:matrix.example.tld')
        room_simulator.add_room('!existingroomid:matrix.example.tld', '#existingroom:matrix.example.tld')
        monkeypatch.setenv('ROOM_SIMULATOR', room_simulator.export())
        # Setup ClientSimulator
        client_simulator = ClientSimulator()
        client_simulator.join('!existingroomid:matrix.example.tld')
        monkeypatch.setenv('CLIENT_SIMULATOR', client_simulator.export())

    def test_room_no_changes_success(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'alias': '#existingroom:matrix.example.tld',
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_room.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is False)

    def test_room_join_success(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'alias': '#myroom:matrix.example.tld',
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_room.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(ansible_result['room_id'] == '#myroom:matrix.example.tld')

    def test_room_join_fail(self, monkeypatch):
        class TestClass(failure.RoomJoin, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'alias': '#myroom:matrix.example.tld',
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_room.main()
        ansible_result = result.value.result

    def test_room_create_success(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'alias': '#mynewroom:matrix.example.tld',
        })
        with pytest.raises(AnsibleExitJson) as result:
            matrix_room.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)
        assert_expression(isinstance(re.match(r"!.*\:matrix\.example\.tld", ansible_result['room_id']), re.Match))

    def test_room_create_fail(self, monkeypatch):
        class TestClass(failure.RoomCreate, MatrixNioSuccess):
            pass
        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'password': 'supersecretpassword',
            'alias': '#mynewroom:matrix.example.tld',
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_room.main()
        ansible_result = result.value.result
