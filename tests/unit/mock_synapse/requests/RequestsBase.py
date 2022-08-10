import abc
import os
import json as json_parser
import requests


class RequestsBase(metaclass=abc.ABCMeta):

    @staticmethod
    @abc.abstractmethod
    def get(url, params=None, **kwargs):
        r"""Sends a GET request.

        :param url: URL for the new :class:`Request` object.
        :param params: (optional) Dictionary, list of tuples or bytes to send
            in the query string for the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_GET_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response

    @staticmethod
    @abc.abstractmethod
    def options(url, **kwargs):
        r"""Sends an OPTIONS request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_OPTIONS_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response

    @staticmethod
    @abc.abstractmethod
    def head(url, **kwargs):
        r"""Sends a HEAD request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes. If
            `allow_redirects` is not provided, it will be set to `False` (as
            opposed to the default :meth:`request` behavior).
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_HEAD_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response

    @staticmethod
    @abc.abstractmethod
    def post(url, data=None, json=None, **kwargs):
        r"""Sends a POST request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_POST_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response

    @staticmethod
    @abc.abstractmethod
    def put(url, data=None, **kwargs):
        r"""Sends a PUT request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_PUT_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response

    @staticmethod
    @abc.abstractmethod
    def patch(url, data=None, **kwargs):
        r"""Sends a PATCH request.

        :param url: URL for the new :class:`Request` object.
        :param data: (optional) Dictionary, list of tuples, bytes, or file-like
            object to send in the body of the :class:`Request`.
        :param json: (optional) json data to send in the body of the :class:`Request`.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_PATCH_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response

    @staticmethod
    @abc.abstractmethod
    def delete(url, **kwargs):
        r"""Sends a DELETE request.

        :param url: URL for the new :class:`Request` object.
        :param \*\*kwargs: Optional arguments that ``request`` takes.
        :return: :class:`Response <Response>` object
        :rtype: requests.Response
        """
        data: dict = json_parser.loads(os.environ.get('REQUESTS_DELETE_RESPONSE', '{}'))
        response_data: dict = data.get(url, {})

        response = requests.Response()
        response.url = url
        response.status_code = response_data.get('status', 200)
        response.encoding = response_data.get('encoding', 'UTF-8')
        response._content = bytes(response_data.get('content', ''), response.encoding)
        print(url)
        return response
