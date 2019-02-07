import logging
import sys

LOG_FORMAT = '%(name)s -> %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s'

def config_logger():
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)

    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler('logs/test.log', mode='w')
    # c_handler.setLevel(logging.INFO)
    # f_handler.setLevel(logging.INFO)
    
    c_format = logging.Formatter(LOG_FORMAT)
    f_format = logging.Formatter(LOG_FORMAT)
    c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)

    logger.info('Config')

    return logger

def foo():
    logger = logging.getLogger(__name__)
    logger.info('Some text')

def get_logger():
    return logging.getLogger('log')

if __name__ == '__main__':
    logger = config_logger()
    logger = logging.getLogger(__name__)
    # logging.basicConfig(level=logging.INFO, format=LOG_FORMAT)
    logger.info('Message 1')
    logger.info('Message 2')
    logger.info('Message 3')
    foo()