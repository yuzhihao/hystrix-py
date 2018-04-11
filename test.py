import functools
import threading
import unittest

import time

import thread

from hystrix_command import HystrixCommand
from hystrix_config import logger
from hystrix import addHystrix

class MyHystrixCommand(HystrixCommand):
    def __init__(self,*args, **kwargs):
        print "init Myhystrix Command"
        HystrixCommand.__init__(self, *args,**kwargs)

class Test():

    def __init__(self):
        self.count =1
    def failback(self, b):
        logger.info('custome fall back')
        return 1,2

    def condition(self, a, b):
        self.count+=1
        self.cond = True
        if self.count == 10:
            self.cond = False
        return self.cond

    @addHystrix(groupKey='group1',
                key='hello1',
                failback=failback)
    def hello(self):
        time.sleep(0.1)
        logger.info('hello1')
        raise Exception()

    @addHystrix(groupKey='group1',
                key='hello1',
                failback=failback)
    def hello1(self):
        time.sleep(0.1)
        logger.info('hello1 pass')

    @addHystrix(groupKey='group1',
                key='hello2')
    def hello2(self):
        time.sleep(0.1)
        logger.info('hello2')

    @addHystrix(groupKey='group1',
                key='hello1')
    def hello3(self):
        time.sleep(0.5)
        logger.info('hello3')

    @addHystrix(groupKey='group1',
                key='hello2')
    def hello4(self):
        time.sleep(0.5)
        logger.info('hello4')

    @addHystrix(
        groupKey='group1',
        key='hello1',
        hystrix_command_class=MyHystrixCommand,
        hystrix_pre_condition=condition,
        hystrix_failback=failback,
        hystrix_fail_threshold=10,
        hystrix_retry_interval=40,
        hystrix_retry_fail_threshold=100
        )
    def hello5(self, a, b):
        logger.info('hello5')

    def testHystrix1(self):
        for i in xrange(100,200):
            self.hello()

    def testHystrix2(self):
        for i in xrange(100,200):
            self.hello2()

    def testHystrix3(self):
        for i in xrange(100,200):
            self.hello3()

    def testHystrix4(self):
        for i in xrange(100,200):
            self.hello4()

    def testHystrixMultiThread(self):
        thread.start_new_thread(self.testHystrix1,())
        thread.start_new_thread(self.testHystrix2,())
        thread.start_new_thread(self.testHystrix3,())
        thread.start_new_thread(self.testHystrix4,())

    def testHystrix(self):
        i = 0
        while i <= 50:
            i+=1

            self.hello()
        i = 0
        while i <= 50:
            i+=1
            self.hello1()
        i = 0
        while i <= 10:
            i += 1
            self.hello()
            time.sleep(1)
        i = 0
        while i <= 10:
            i += 1
            self.hello1()
            time.sleep(5)

    def testHystrix2(self):
        for i in range(20):
            self.hello5(1,2)
        self.hello5(1,2)

if __name__ == '__main__':
    test = Test()

    test.testHystrix2()

    #test.testHystrixMultiThread()
    #time.sleep(50)