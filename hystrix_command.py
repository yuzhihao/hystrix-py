#!/usr/bin/env python
# -*- coding:utf-8 -*-
# by yuzhihao

from circuit_controller import CircuitController
from hystrix_config import logger, HystrixConfig


class HystrixCommand:
    """ You can custom your own Command by extending this class  
    """

    def __init__(self, *args, **kwargs):
        fail_threshold = kwargs.pop('hystrix_fail_threshold',HystrixConfig.fail_threshold)
        retry_interval = kwargs.pop('hystrix_retry_interval', HystrixConfig.retry_interval)
        retry_fail_threshold = kwargs.pop('hystrix_retry_fail_threshold', HystrixConfig.retry_fail_threshold)
        self.circuitController = CircuitController(fail_threshold=fail_threshold,
                                                   retry_interval=retry_interval,
                                                   retry_fail_threshold=retry_fail_threshold)

    def execute(self, func, *args, **kwargs):
        condition = kwargs.pop('hystrix_pre_condition', self._default_condition)
        failback = kwargs.pop('hystrix_failback', self._defalut_failback)
        user_kwargs = {}
        for k, v in kwargs.items():
            if not k.startswith('hystrix_'):
                user_kwargs[k] = v
        # check pre_condition first，then the circurt state
        if condition(*args, **user_kwargs) and self.circuitController.check_state():
            try:
                result = func(*args, **user_kwargs)
                self.circuitController.on_success()
                return result
            except Exception as e:
                logger.error("exception:".format(e.message))
                self.circuitController.on_failure()
                return failback(*args, ** user_kwargs)
        else:
            return failback(*args, ** user_kwargs)

    def _defalut_failback(self,*args, **kwargs):
        """ default failback function"""
        logger.info('defalut failback')

    def _default_condition(self, *args, **kwargs):
        """ default condition function"""
        return True


