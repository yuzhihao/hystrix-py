#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading

from hystrix_command import HystrixCommand


class HystrixGroup:

    def __init__(self, groupKey=None):
        self.groupKey =  groupKey
        self.commands = {}
        self.lock =  threading.Lock()

    def getCommand(self, key):
        with self.lock:
            if self.commands.get(key):
                return self.commands.get(key)
            else:
                command = HystrixCommand()
                self.commands[key] = command
                return command
