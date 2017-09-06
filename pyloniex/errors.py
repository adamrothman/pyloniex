# -*- coding: utf-8 -*-


class PoloniexAPIError(Exception):

    def __init__(self, status_code: int, message: str) -> None:
        self.status_code = status_code
        self.message = message

    def __str__(self):
        return f'[{self.status_code}] {self.message}'
