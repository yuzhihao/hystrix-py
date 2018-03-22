#!/usr/bin/env python
# -*- coding:utf-8 -*-

from circuit_controller import CircuitController
from hystrix_config import logger, HystrixConfig


class HystrixCommand:

    def __init__(self):
        self.circuitController = CircuitController(fail_threshold=HystrixConfig.fail_threshold,
                                                   retry_interval=HystrixConfig.retry_interval,
                                                   retry_fail_threshold=HystrixConfig.retry_fail_threshold,)

    def execute(self, func, *args, **kwargs):
        failback = kwargs.pop('failback', self._defalut_failback)
        if self.circuitController.check_state():
            try:
                result = func(*args, **kwargs)
                self.circuitController.on_success()
                return result
            except Exception as e:
                logger.error("exception:".format(e.message))
                self.circuitController.on_failure()
                return failback(*args, ** kwargs)
        else:
            return failback(*args, ** kwargs)

    def _defalut_failback(self,*args, **kwargs):
        """ default failback function"""
        logger.info('defalut failback')


