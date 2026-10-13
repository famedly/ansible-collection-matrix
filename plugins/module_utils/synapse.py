# coding: utf-8

# (c) 2021, Famedly GmbH
# GNU Affero General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/agpl-3.0.txt)

from __future__ import absolute_import, division, print_function

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
    def __init__(
        self, home_server: str, access_token: str, api_prefix: str = "_synapse/admin/"
    ):
        self.api_prefix = api_prefix
        self.home_server = home_server
        self.access_token = access_token

        # Prepare URLs
        self.api_url = urllib.parse.urljoin(self.home_server, self.api_prefix)

        # init subclasses
        self.join = self.__Join(self)

    # Make API request
    def get(self, path: str) -> requests.Response:
        response = requests.get(
            url=urllib.parse.urljoin(self.api_url, path),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code == 200:
            return response
        if response.status_code == 500:
            raise Exceptions.MatrixException(
                f"Matrix Error\nHTTP-Code: {response.status_code}\n Response: {response.text}"
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected return code\nHTTP-Code: {response.status_code}\n Response: {response.text}"
            )

    def post(self, path: str, **kwargs) -> requests.Response:
        response = requests.post(
            url=urllib.parse.urljoin(self.api_url, path),
            headers={"Authorization": f"Bearer {self.access_token}"},
            **kwargs,
        )
        if response.status_code == 200:
            return response
        if response.status_code == 500:
            raise Exceptions.MatrixException(
                f"Matrix Error\nHTTP-Code: {response.status_code}\n Response: {response.text}"
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected return code\nHTTP-Code: {response.status_code}\n Response: {response.text}"
            )

    def delete(self, path: str) -> requests.Response:
        response = requests.delete(
            url=urllib.parse.urljoin(self.api_url, path),
            headers={"Authorization": f"Bearer {self.access_token}"},
        )
        if response.status_code == 200:
            return response
        if response.status_code == 500:
            raise Exceptions.MatrixException(
                f"Matrix Error\nHTTP-Code: {response.status_code}\n Response: {response.text}"
            )
        else:
            raise Exceptions.HTTPException(
                f"Unexpected return code\nHTTP-Code: {response.status_code}\n Response: {response.text}"
            )

    @staticmethod
    def url_encode(string: str) -> str:
        return urllib.parse.quote(string)

    class __Join:
        API_PATH = "v1/join/{room_id}"

        def __init__(self, parent):
            self.__parent = parent

        def join(self, room_id: str, user_id: str) -> dict:
            room_id = AdminApi.url_encode(room_id)
            return self.__parent.post(
                self.API_PATH.format(room_id=room_id),
                json={"user_id": user_id},
            ).json()


class Exceptions:
    class HTTPException(BaseException):
        def __init__(self, *args):
            super().__init__(*args)

    class MatrixException(BaseException):
        def __init__(self, *args):
            super().__init__(*args)
