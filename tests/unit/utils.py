import json
from typing import Union

from ansible.module_utils import basic
from ansible.module_utils._text import to_bytes


class AnsibleExitJson(Exception):
    def __init__(self, result: Union[dict, list], *args):
        self.result = result
        super().__init__(*args)


class AnsibleFailJson(Exception):
    def __init__(self, result: Union[dict, list], *args):
        self.result = result
        super().__init__(*args)


def set_module_args(args):
    if "_ansible_remote_tmp" not in args:
        args["_ansible_remote_tmp"] = "/tmp"
    if "_ansible_keep_remote_files" not in args:
        args["_ansible_keep_remote_files"] = False

    args = json.dumps({"ANSIBLE_MODULE_ARGS": args})
    basic._ANSIBLE_ARGS = to_bytes(args)


def exit_json(*args, **kwargs):
    """function to patch over exit_json; package return data into an exception"""
    if "changed" not in kwargs:
        kwargs["changed"] = False
    raise AnsibleExitJson(kwargs)


def fail_json(*args, **kwargs):
    """function to patch over fail_json; package return data into an exception"""
    kwargs["failed"] = True
    raise AnsibleFailJson(kwargs)


def assert_expression(expression):
    if not expression:
        raise AssertionError()
