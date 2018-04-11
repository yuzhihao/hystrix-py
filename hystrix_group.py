#!/usr/bin/env python
# -*- coding:utf-8 -*-

import threading

from hystrix_command import HystrixCommand


class HystrixGroup:

    def __init__(self, groupKey=None):
        self.groupKey =  groupKey
        self.commands = {}
        self.lock =  threading.Lock()

    def getCommand(self, key, *args, **kwargs):
        with self.lock:
            if self.commands.get(key):
                return self.commands.get(key)
            else:
                cls = kwargs.pop('hystrix_command_class', HystrixCommand)
                print "init command:", cls
                command = cls(*args, **kwargs)
                self.commands[key] = command
                return command
