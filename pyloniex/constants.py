# -*- coding: utf-8 -*-
from enum import Enum


class OrderType(str, Enum):
    fill_or_kill = 'fillOrKill'
    immediate_or_cancel = 'immediateOrCancel'
    post_only = 'postOnly'
