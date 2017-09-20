# -*- coding: utf-8 -*-
from typing import Optional

from requests import PreparedRequest
from requests import Response


class PoloniexAPIError(Exception):

    def __init__(self, response: Response) -> None:
        self._response = response
        self._message = None

        data = None
        try:
            data = response.json()
        except ValueError:
            pass
        if isinstance(data, dict):
            self._message = data.get('error')

    def __str__(self):
        s = f'[{self.status_code}]'
        if self.message is not None:
            s += f' {self.message}'
        return s

    @property
    def request(self) -> PreparedRequest:
        return self._response.request

    @property
    def response(self) -> Response:
        return self._response

    @property
    def status_code(self) -> int:
        return self._response.status_code

    @property
    def message(self) -> Optional[str]:
        return self._message


class PoloniexRequestError(PoloniexAPIError):
    pass


class PoloniexServerError(PoloniexAPIError):
    pass
