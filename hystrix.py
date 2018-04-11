#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by zhihaoyu

import functools
import threading

from hystrix_command import HystrixCommand
from hystrix_config import logger
from hystrix_group import HystrixGroup



def addHystrix(*args, **kwargs):
    """ hystrix wrapper 
        you can easily add hystrix functions using this wrapper. It is thread safe 
        kwargs:
            groupKey='group1', 
            key='hello1',
            hystrix_command_class: your own command class extending HystrixCommand, 
            hystrix_pre_condition: a function runs first and it returns true or false,
            hystrix_failback: a function that runs when your function raises exception,
            hystrix_fail_threshold: fail count after which circuit closes
            hystrix_retry_interval: time interval after which retry
            hystrix_retry_fail_threshold: fail counts after which retry
    """
    newKwargs = kwargs
    def function_wrap(func):
        @functools.wraps(func)
        def wrapped_func(*args, **kwargs):
            #kwargs['_hystrix_kwargs'] = newKwargs
            kwargs.update(newKwargs)
            return Hystrix._hystrix(func, *args, **kwargs)
        return wrapped_func
    return function_wrap

class Hystrix:

    # 待使用 TODO
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
        command = group.getCommand(key, *args, **kwargs)
        # 线程池的控制待添加 TODO
        return command.execute(func, *args, **kwargs)

