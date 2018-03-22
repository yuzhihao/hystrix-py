import logging

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                datefmt='%a, %d %b %Y %H:%M:%S',
                filename='test.log',
                filemode='w')

console = logging.StreamHandler()
console.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(levelname)-8s %(message)s')
console.setFormatter(formatter)
logger = logging.getLogger('test')
logger.addHandler(console)


class HystrixConfig:
    # threshold of fail requests counts, after which the state turn to Close
    fail_threshold = 5
    # time interval of another request after circuit close
    retry_interval = 30
    # counts of requests in Close state
    retry_fail_threshold = 50
