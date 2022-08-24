from __future__ import absolute_import, division, print_function, annotations

import types

import pytest
from _pytest.monkeypatch import MonkeyPatch
from ansible_collections.famedly.matrix.tests.unit.mock_nio.client import failure
from ansible_collections.famedly.matrix.tests.unit.mock_nio.client import success

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import (
    matrix_login,
    matrix_logout,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioBase import (
    MatrixNioBase,
)
from ansible_collections.famedly.matrix.tests.unit.mock_nio.MatrixNioSuccess import (
    MatrixNioSuccess,
)
from ansible_collections.famedly.matrix.tests.unit.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    assert_expression,
    set_module_args,
    exit_json,
    fail_json,
)


class TestAnsibleNioModule:
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

    # Success tests
    def test_matrix_nio_module_login_usr_passwd(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_login.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is False)
        assert_expression(ansible_result["token"] == MatrixNioBase.ACCESS_TOKEN)

    def test_matrix_nio_module_login_token(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": MatrixNioBase.ACCESS_TOKEN,
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_login.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is False)
        assert_expression(ansible_result["token"] == MatrixNioBase.ACCESS_TOKEN)

    def test_matrix_nio_module_logout_usr_passwd(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_logout.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is False)

    def test_matrix_nio_module_logout_token(self, monkeypatch):
        self.patchAnsibleNioModule(monkeypatch, MatrixNioSuccess)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "token": MatrixNioBase.ACCESS_TOKEN,
            }
        )
        with pytest.raises(AnsibleExitJson) as result:
            matrix_logout.main()
        ansible_result = result.value.result
        assert_expression(ansible_result["changed"] is False)

    def test_matrix_nio_module_login_fail(self, monkeypatch):
        class TestClass(failure.ClientLogin, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_login.main()

    def test_matrix_nio_module_logout_fail(self, monkeypatch):
        class TestClass(failure.ClientLogout, MatrixNioSuccess):
            pass

        self.patchAnsibleNioModule(monkeypatch, TestClass)
        monkeypatch.setattr(matrix.AsyncClient, "logged_in", True)
        set_module_args(
            {
                "hs_url": "matrix.example.tld",
                "user_id": "myuser",
                "password": "supersecretpassword",
            }
        )
        with pytest.raises(AnsibleFailJson) as result:
            matrix_logout.main()
