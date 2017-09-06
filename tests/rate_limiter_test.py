# -*- coding: utf-8 -*-
import time
from collections import Counter

from pyloniex.utils import RateLimiter


def test_rate_limiter():
    limiter = RateLimiter(4, 1, 1)
    counter = Counter()

    while True:
        now = time.time()
        bucket = int(now)
        if limiter.check('test') is True:
            counter[bucket] += 1
        if len(counter) > 4:
            break
        time.sleep(0.01)

    for bucket, count in counter.items():
        assert count <= 4

    print()
    print(counter)
