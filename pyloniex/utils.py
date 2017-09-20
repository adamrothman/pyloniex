# -*- coding: utf-8 -*-
from collections import OrderedDict
from time import time
from typing import Any
from typing import Dict
from typing import Tuple


def protect_floats(params: Dict[str, Any]) -> Dict[str, Any]:
    """Python's default behavior for stringifying small floats is to use
    scientific notation.

        >>> str(0.00000001)
        '1e-08'

    This is a bummer for us. Poloniex uses 8 points of precision, so that's how
    we roll.
    """
    return {
        k: (f'{v:.8f}' if isinstance(v, float) else v)
        for k, v
        in params.items()
    }


class RateLimiter:
    """A very fast rate in-memory rate limiter using the token bucket
    algorithm. See https://en.wikipedia.org/wiki/Token_bucket for details.

    Tokens accumulate in the bucket at a constant rate per second, given by
    `per_second`. Each time RateLimiter::check is called, one token is removed
    from the bucket.

    The `burst` parameter controls the maximum number of tokens that may be
    held by the bucket at once. If tokens are not removed, they will accumulate
    up to this limit.

    Events are identified by a key (so a single RateLimiter instance can limit
    multiple kinds of events, or events from multiple sources, etc.). `size`
    limits the number of keys that can be tracked. If this limit is reached,
    the oldest key will be evicted.

    If you just want to limit some event(s) to no more than X times per second,
    set `per_second` := X and `burst` := 1.

    If unused capacity can be "banked" for increased usage later, set `burst`
    to some value > 1.
    """

    def __init__(self, per_second: float, burst: float, size: int) -> None:
        self._per_second = per_second
        self._burst = burst
        self._size = size
        self._buckets: OrderedDict[str, Tuple[float, float]] = OrderedDict()

    def check(self, key: str) -> bool:
        now = time()
        budget, timestamp = self._buckets.get(key, (self._burst, now))
        budget = min(self._burst, budget + (now - timestamp) * self._per_second) - 1
        if budget < 0:
            return False

        if key in self._buckets:
            del self._buckets[key]
        elif len(self._buckets) >= self._size:
            self._buckets.popitem(last=False)

        self._buckets[key] = (budget, now)
        return True
