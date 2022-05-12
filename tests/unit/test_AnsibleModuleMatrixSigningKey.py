from __future__ import (absolute_import, division, print_function, annotations)

import os
import re
from tempfile import NamedTemporaryFile

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import matrix
from ansible_collections.famedly.matrix.plugins.modules import matrix_signing_key
from ansible_collections.famedly.matrix.tests.unit.utils import AnsibleExitJson, AnsibleFailJson, set_module_args, \
    exit_json, fail_json, assert_expression


class TestAnsibleModuleMatrixSigningKey():
    @staticmethod
    def patchModule(monkeypatch: MonkeyPatch):
        monkeypatch.setattr(matrix.AnsibleModule, 'exit_json', exit_json)
        monkeypatch.setattr(matrix.AnsibleModule, 'fail_json', fail_json)

    def test_no_change(self, monkeypatch):
        self.patchModule(monkeypatch)
        with NamedTemporaryFile() as temp_file:
            set_module_args({
                'path': temp_file.name,
            })
            with pytest.raises(AnsibleExitJson) as result:
                matrix_signing_key.main()
            ansible_result = result.value.result
            assert_expression(ansible_result['changed'] is False)

    def test_create_key_success(self, monkeypatch):
        self.patchModule(monkeypatch)
        with NamedTemporaryFile() as temp_file:
            os.unlink(temp_file.name)
            set_module_args({
                'path': temp_file.name,
            })
            with pytest.raises(AnsibleExitJson) as result:
                matrix_signing_key.main()
            ansible_result = result.value.result
            assert_expression(ansible_result['changed'] is True)
            with open(temp_file.name, 'r') as f:
                key_file = f.read()
            assert_expression(isinstance(re.match(r"ed25519 .* .{43}", key_file), re.Match))

    def test_create_key_fail(self, monkeypatch):
        self.patchModule(monkeypatch)
        set_module_args({
            'path': '/invalid/path',
        })
        with pytest.raises(AnsibleFailJson) as result:
            matrix_signing_key.main()
