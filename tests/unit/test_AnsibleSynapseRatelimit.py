from __future__ import (absolute_import, division, print_function, annotations)

import json
import types

import pytest
from _pytest.monkeypatch import MonkeyPatch

from ansible_collections.famedly.matrix.plugins.module_utils import synapse
from ansible_collections.famedly.matrix.plugins.modules import synapse_ratelimit
from ansible_collections.famedly.matrix.tests.unit.mock_synapse.requests.RequestsBase import RequestsBase
from ansible_collections.famedly.matrix.tests.unit.utils import AnsibleExitJson, AnsibleFailJson, assert_expression, \
    set_module_args, exit_json, fail_json


class TestAnsibleSynapseRatelimit:
    @staticmethod
    def patchModule(monkeypatch: MonkeyPatch, target_module, mock_class: type(RequestsBase)):
        # Mock ansible functions
        monkeypatch.setattr(target_module.AnsibleModule, 'exit_json', exit_json)
        monkeypatch.setattr(target_module.AnsibleModule, 'fail_json', fail_json)
        # Mock MatrixNio
        for method in RequestsBase.__dict__:
            if isinstance(getattr(mock_class, method), (types.FunctionType, types.BuiltinFunctionType)):
                monkeypatch.setattr(synapse.requests, method, getattr(mock_class, method))

    # Success tests
    def test_synapse_ratelimit_get(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 0,"burst_count": 0}'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'get',
        })
        with pytest.raises(AnsibleExitJson) as result:
            synapse_ratelimit.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is False)

    def test_synapse_ratelimit_set_changes(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        get_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 0,"burst_count": 0}'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(get_response))
        post_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 10,"burst_count": 10}'
            }
        }
        monkeypatch.setenv('REQUESTS_POST_RESPONSE', json.dumps(post_response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'set',
            'messages_per_second': 10,
            'burst_count': 10,
        })
        with pytest.raises(AnsibleExitJson) as result:
            synapse_ratelimit.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)

    def test_synapse_ratelimit_set_no_changes(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        get_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 10,"burst_count": 10}'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(get_response))
        post_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 10,"burst_count": 10}'
            }
        }
        monkeypatch.setenv('REQUESTS_POST_RESPONSE', json.dumps(post_response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'set',
            'messages_per_second': 10,
            'burst_count': 10,
        })
        with pytest.raises(AnsibleExitJson) as result:
            synapse_ratelimit.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is False)

    def test_synapse_ratelimit_delete(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        get_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 10,"burst_count": 10}'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(get_response))
        delete_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{}'
            }
        }
        monkeypatch.setenv('REQUESTS_DELETE_RESPONSE', json.dumps(delete_response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'delete',
        })
        with pytest.raises(AnsibleExitJson) as result:
            synapse_ratelimit.main()
        ansible_result = result.value.result
        assert_expression(ansible_result['changed'] is True)

    def test_synapse_ratelimit_get_failure(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 500,
                'content': 'mocked failure'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'get',
        })
        with pytest.raises(AnsibleFailJson) as result:
            synapse_ratelimit.main()

    def test_synapse_ratelimit_set_failure(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        get_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 0,"burst_count": 0}'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(get_response))
        post_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 500,
                'content': 'mocked failure'
            }
        }
        monkeypatch.setenv('REQUESTS_POST_RESPONSE', json.dumps(post_response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'set',
            'messages_per_second': 10,
            'burst_count': 10,
        })
        with pytest.raises(AnsibleFailJson) as result:
            synapse_ratelimit.main()

    def test_synapse_ratelimit_delete_failure(self, monkeypatch):
        self.patchModule(monkeypatch, synapse_ratelimit, RequestsBase)
        get_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 200,
                'content': '{"messages_per_second": 0,"burst_count": 0}'
            }
        }
        monkeypatch.setenv('REQUESTS_GET_RESPONSE', json.dumps(get_response))
        delete_response = {
            '_synapse/admin/v1/users/myuser/override_ratelimit': {
                'status': 500,
                'content': 'mocked failure'
            }
        }
        monkeypatch.setenv('REQUESTS_DELETE_RESPONSE', json.dumps(delete_response))
        set_module_args({
            'hs_url': 'matrix.example.tld',
            'user_id': 'myuser',
            'access_token': 'supersecrettoken',
            'action': 'delete',
        })
        with pytest.raises(AnsibleFailJson) as result:
            synapse_ratelimit.main()
