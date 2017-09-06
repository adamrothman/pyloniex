# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
from time import sleep
from typing import Any
from typing import Dict
from typing import List
from typing import Union

from requests import Request
from requests import Session

from pyloniex.errors import PoloniexAPIError
from pyloniex.utils import RateLimiter


REQUESTS_PER_SECOND = 6


class PoloniexBaseAPI(metaclass=ABCMeta):

    @abstractmethod
    def __init__(
        self,
        *,
        requests_per_second: int = REQUESTS_PER_SECOND,
    ) -> None:
        self._rate_limiter = RateLimiter(
            requests_per_second,
            requests_per_second,
            1,
        )
        self._requests_per_second = requests_per_second
        self._session = Session()

    def request(
        self,
        *args,
        **kwargs,
    ) -> Union[Dict[str, Any], List[Dict[str, Any]]]:
        cls_name = type(self).__name__
        while self._rate_limiter.check(cls_name) is False:
            sleep(1 / self._requests_per_second)

        request = Request(*args, **kwargs)
        prepared = self._session.prepare_request(request)

        response = self._session.send(prepared)
        data = response.json()
        if 'error' in data:
            raise PoloniexAPIError(response.status_code, data['error'])

        return data
