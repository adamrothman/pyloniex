# -*- coding: utf-8 -*-
import time
from collections import Counter

from pyloniex.utils import RateLimiter


def test_rate_limiter():
    max_per_sec = 6

    limiter = RateLimiter(max_per_sec, 1, 1)
    counter = Counter()

    while True:
        now = time.time()
        bucket = int(now)
        if limiter.check('test') is True:
            counter[bucket] += 1
        if len(counter) > 4:
            break

    for bucket, count in counter.items():
        assert count <= max_per_sec
