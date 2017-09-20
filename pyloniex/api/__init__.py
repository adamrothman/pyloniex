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

import tenacity
from requests import Request
from requests import Session

from pyloniex.errors import PoloniexRequestError
from pyloniex.errors import PoloniexServerError
from pyloniex.utils import RateLimiter


REQUESTS_PER_SECOND = 6

logger = getLogger(__name__)


def _retry_poloniex_error(exc):
    if isinstance(exc, PoloniexRequestError) and exc.status_code == 429:
        return True
    elif isinstance(exc, PoloniexServerError):
        return True
    return False


class PoloniexBaseAPI(metaclass=ABCMeta):

    @abstractmethod
    def __init__(
        self,
        *,
        requests_per_second: int = REQUESTS_PER_SECOND,
    ) -> None:
        self._rate_limiter = RateLimiter(requests_per_second, 1, 1)
        self._requests_per_second = requests_per_second
        self._session = Session()

    @tenacity.retry(
        retry=tenacity.retry_if_exception(_retry_poloniex_error),
        wait=tenacity.wait_exponential() + tenacity.wait_random(0, 1),
        stop=tenacity.stop_after_attempt(4) | tenacity.stop_after_delay(8),
        reraise=True,
    )
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

        status = response.status_code
        if status >= 200 and status < 300:
            data = None
            try:
                data = response.json()
            except ValueError:
                logger.exception('Error decoding response JSON')
            return data
        elif status >= 400 and status < 500:
            raise PoloniexRequestError(response)
        elif status >= 500:
            raise PoloniexServerError(response)
        else:
            # We shouldn't ever get 1xx responses (Poloniex doesn't send them)
            # or 3xx responses (requests follows redirects); return None to
            # make mypy happy
            return None
