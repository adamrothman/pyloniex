# -*- coding: utf-8 -*-
from typing import Optional


class PoloniexAPIError(Exception):

    def __init__(
        self,
        status_code: int,
        message: Optional[str] = None,
    ) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self):
        s = f'[{self.status_code}]'
        if self.message is not None:
            s += f' {self.message}'
        return s


class PoloniexRequestError(PoloniexAPIError):
    pass


class PoloniexServerError(PoloniexAPIError):
    pass
