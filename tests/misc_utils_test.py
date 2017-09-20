# -*- coding: utf-8 -*-
from pyloniex.utils import protect_floats


def test_protect_floats():
    stuff = {'a': 'b', 'c': 1, 'd': 7.1e-07}
    assert protect_floats(stuff) == {'a': 'b', 'c': 1, 'd': '0.00000071'}
