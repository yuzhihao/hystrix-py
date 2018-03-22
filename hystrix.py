#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by zhihaoyu

import functools
import threading

from hystrix_config import logger
from hystrix_group import HystrixGroup



def addHystrix(*args, **kwargs):
    """ hystrix wrapper """

    newKwargs = kwargs
    def function_wrap(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            kwargs.update(newKwargs)
            return Hystrix._hystrix(func, *args, **kwargs)
        return wrapped_func
    return function_wrap

class Hystrix:

    # 待使用
    hystrixThreadPools = {}
    commands = {}
    groups = {}
    group_lock = threading.Lock()

    def __init__(self, *args, **kwargs):
        pass

    @classmethod
    def _getGroup(cls, groupKey):
        with cls.group_lock:
            if cls.groups.get(groupKey):
                return cls.groups[groupKey]
            logger.debug("Creating new group for groupKey:%s", groupKey)

            group = HystrixGroup()
            cls.groups[groupKey] = group
            return group

    @classmethod
    def _hystrix(cls, func, *args, **kwargs):
        groupKey = kwargs.pop('groupKey','default')
        key = kwargs.pop('key','default')
        group = cls._getGroup(groupKey)
        command = group.getCommand(key)
        # 线程池的控制待添加
        return command.execute(func, *args, **kwargs)

