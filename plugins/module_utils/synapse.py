# coding: utf-8

# (c) 2021, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

import traceback
import urllib.parse
from types import SimpleNamespace

# Check if all required libs can load
LIB_IMP_ERR = None
try:
    import requests
    HAS_REQUESTS = True
except ImportError:
    REQUESTS_IMPORT_ERROR = traceback.format_exc()
    HAS_REQUESTS = False
    requests = SimpleNamespace(Response=None)


class AdminApi:
    def __init__(self,
                 home_server: str,
                 access_token: str,
                 api_prefix: str = "_synapse/admin/"):
        self.api_prefix = api_prefix
        self.home_server = home_server
        self.access_token = access_token

        # Prepare URLs
        self.api_url = urllib.parse.urljoin(self.home_server, self.api_prefix)

        # init subclasses
        self.ratelimit = self.__Ratelimit(self)

    # Make API request
    def get(self, path: str) -> requests.Response:
        response = requests.get(url=urllib.parse.urljoin(self.api_url, path),
                                headers={"Authorization": f"Bearer {self.access_token}"})
        if response.status_code == 200:
            return response
        if response.status_code == 500:
            raise Exceptions.MatrixException(
                f"Matrix Error\nHTTP-Code: {response.status_code}\n Response: {response.text}")
        else:
            raise Exceptions.HTTPException(
                f"Unexpected return code\nHTTP-Code: {response.status_code}\n Response: {response.text}")

    def post(self, path: str, **kwargs) -> requests.Response:
        response = requests.post(url=urllib.parse.urljoin(self.api_url, path),
                                 headers={"Authorization": f"Bearer {self.access_token}"}, **kwargs)
        if response.status_code == 200:
            return response
        if response.status_code == 500:
            raise Exceptions.MatrixException(
                f"Matrix Error\nHTTP-Code: {response.status_code}\n Response: {response.text}")
        else:
            raise Exceptions.HTTPException(
                f"Unexpected return code\nHTTP-Code: {response.status_code}\n Response: {response.text}")

    def delete(self, path: str) -> requests.Response:
        response = requests.delete(url=urllib.parse.urljoin(self.api_url, path),
                                   headers={"Authorization": f"Bearer {self.access_token}"})
        if response.status_code == 200:
            return response
        if response.status_code == 500:
            raise Exceptions.MatrixException(
                f"Matrix Error\nHTTP-Code: {response.status_code}\n Response: {response.text}")
        else:
            raise Exceptions.HTTPException(
                f"Unexpected return code\nHTTP-Code: {response.status_code}\n Response: {response.text}")

    @staticmethod
    def url_encode(string: str) -> str:
        return urllib.parse.quote(string)

    # TODO: extend for each API-Method
    class __Ratelimit:
        API_PATH = "v1/users/{user_id}/override_ratelimit"

        def __init__(self, parent):
            self.__parent = parent

        def get(self, user_id: str) -> dict:
            user_id = AdminApi.url_encode(user_id)
            return self.__parent.get(self.API_PATH.format(user_id=user_id)).json()

        def set(self, user_id: str, messages_per_second: int = 0, burst_count: int = 0) -> dict:
            user_id = AdminApi.url_encode(user_id)
            return self.__parent.post(
                self.API_PATH.format(user_id=user_id), json={"messages_per_second": messages_per_second,
                                                             "burst_count": burst_count}).json()

        def delete(self, user_id: str) -> dict:
            user_id = AdminApi.url_encode(user_id)
            return self.__parent.delete(self.API_PATH.format(user_id=user_id)).json()


class Exceptions:
    class HTTPException(BaseException):
        def __init__(self, *args):
            super().__init__(*args)

    class MatrixException(BaseException):
        def __init__(self, *args):
            super().__init__(*args)
