import functools
import threading
import unittest

import time

import thread

from hystrix_config import logger
from hystrix import addHystrix


class Test():

    def failback(self):
        logger.info('custome fall back')
        return 1,2

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
        thread.start_new_thread(self.testHystrix4, ())

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

if __name__ == '__main__':
    test = Test()

    test.testHystrix()

    #test.testHystrixMultiThread()
    #time.sleep(50)