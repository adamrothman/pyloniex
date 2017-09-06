# -*- coding: utf-8 -*-
from abc import ABCMeta
from abc import abstractmethod
from time import sleep
from logging import getLogger
from typing import Any
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from requests import Request
from requests import Session

from pyloniex.errors import PoloniexRequestError
from pyloniex.errors import PoloniexServerError
from pyloniex.utils import RateLimiter


REQUESTS_PER_SECOND = 6

logger = getLogger(__name__)


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
    ) -> Optional[Union[Dict[str, Any], List[Dict[str, Any]]]]:
        cls_name = type(self).__name__
        while self._rate_limiter.check(cls_name) is False:
            sleep(1 / self._requests_per_second)

        request = Request(*args, **kwargs)
        prepared = self._session.prepare_request(request)

        response = self._session.send(prepared)
        try:
            data = response.json()
        except ValueError:
            logger.exception('Error decoding response JSON')
            data = None

        status = response.status_code
        if status >= 200 and status < 300:
            return data

        error = None
        if isinstance(data, dict) and 'error' in data:
            error = data['error']

        if status >= 400 and status < 500:
            raise PoloniexRequestError(status, error)
        elif status >= 500:
            raise PoloniexServerError(status, error)
        else:
            # We never expect to get a 3xx; if we do, just return None
            return None
