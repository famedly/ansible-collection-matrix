from __future__ import absolute_import, division, print_function, annotations

import types

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_notification

from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import (
    MatrixNioBase,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioSuccess import (
    MatrixNioSuccess,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.room import failure
from ansible_collections.famedly.matrix.tests.unit.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    assert_expression,
    set_module_args,
    exit_json,
    fail_json,
)


class TestAnsibleModuleMatrixNotification:
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

    def test_notification_success(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "#myroom:matrix.example.tld",
                "msg_plain": "**hello world**",
                "msg_html": "<b>hello world</b>",
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_notification.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)

    def test_notification_fail(self, monkeypatch):
        class TestClass(failure.RoomSend, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "#myroom:matrix.example.tld",
                "msg_plain": "**hello world**",
                "msg_html": "<b>hello world</b>",
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_notification.main()
        ansible_result = result.value.result

    def test_notification_check_mode(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
                "room_id": "#myroom:matrix.example.tld",
                "msg_plain": "**hello world**",
                "msg_html": "<b>hello world</b>",
            },
            check_mode=True,
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_notification.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
