from __future__ import absolute_import, division, print_function, annotations

import types

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_token_login

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


class TestAnsibleModuleMatrixTokenLogin:
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

    def test_token_login_check_mode(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "key": "static-psk",
            },
            check_mode=True,
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_token_login.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        # If admin was not set, we do not expect any information about admin status
        assert_expression("admin" not in ansible_result)
        assert_expression(ansible_result["device_id"] != "")
        assert_expression(ansible_result["token"] != "")

    def test_token_login_check_mode_admin(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "key": "static-psk",
                "admin": True,
            },
            check_mode=True,
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_token_login.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        assert_expression(ansible_result["admin"] is True)
        assert_expression(ansible_result["device_id"] != "")
        assert_expression(ansible_result["token"] != "")

    def test_token_login_check_mode_demote_admin(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "key": "static-psk",
                "admin": False,
            },
            check_mode=True,
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_token_login.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is True)
        # When admin has been set to false, expect the user to be demoted
        assert_expression(ansible_result["admin"] is False)
        assert_expression(ansible_result["device_id"] != "")
        assert_expression(ansible_result["token"] != "")
