#!/usr/bin/env python
# -*- coding:utf-8 -*-
import threading

import time

from hystrix_config import logger

CIRCIT_CLOSE = 1
CIRCIT_HALF_OPEN = 2
CIRCIT_OPEN = 3

class CircuitController:
    """ circuit controller  
        State transform:  open -> close -> half_open -> open/close 
    """

    def __init__(self, fail_threshold=5,
                 retry_interval=30,
                 retry_fail_threshold=100):
        self._state = CIRCIT_OPEN
        self._fail_threshold = fail_threshold
        self._retry_interval = retry_interval
        self._retry_fail_threshold = retry_fail_threshold

        self._half_open_time = 0
        self._fail_count = 0
        self._retry_fail_count = 0

        self._lock = threading.Lock()

    def _open(self):
        '''Open the circuit and set time for half open'''
        self._state = CIRCIT_OPEN
        self._fail_count = 0
        logger.info("Circuit opene")

    def _close(self):
        '''Close circuit and reset failure count'''
        self._state = CIRCIT_CLOSE
        self._half_open_time = time.time() + self._retry_interval
        self._retry_fail_count = 0
        logger.debug("Circuit close")

    def _half_open(self):
        ''' Set circuit to half open state'''
        self._state = CIRCIT_HALF_OPEN
        logger.debug("Circuit half open")

    def check_state(self):
        '''Check current state and judge rights'''
        with self._lock:
            if self._state == CIRCIT_CLOSE:
                now = time.time()
                self._retry_fail_count += 1
                if now >= self._half_open_time or self._retry_fail_count >= self._retry_fail_threshold:
                    self._half_open()
            return self._state in [CIRCIT_HALF_OPEN,CIRCIT_OPEN]

    def on_failure(self):
        '''
        increase failure counts and change state if _fail_threshold is reached
        '''
        with self._lock:
            if self._state == CIRCIT_HALF_OPEN:
                logger.debug("Fail in Half_open state, close circuit")
                self._close()
            elif self._state == CIRCIT_OPEN:
                self._fail_count += 1
                logger.debug("Fail in open state, fail count: {}".format(self._fail_count))
                if self._fail_count >= self._fail_threshold:
                    if self._state != CIRCIT_CLOSE:
                        self._close()

    def on_success(self):
        '''
        Change state to open if half_open
        '''
        with self._lock:
            if self._state == CIRCIT_HALF_OPEN:
                self._open()

    def upload_info(self):
        """upload infomation"""
