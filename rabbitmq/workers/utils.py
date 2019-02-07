import logging
import sys

LOG_FORMAT = '%(name)s -> %(filename)s:%(funcName)s:%(lineno)d [%(levelname)s] %(message)s'

def config_logger(log_file='logs/service.log', mode='a'):
    logger = logging.getLogger()
    logger.setLevel(logging.NOTSET)
    c_handler = logging.StreamHandler(sys.stdout)
    f_handler = logging.FileHandler(filename=log_file, mode=mode)
    c_handler.setFormatter(logging.Formatter(LOG_FORMAT))
    f_handler.setFormatter(logging.Formatter(LOG_FORMAT))

    logger.addHandler(c_handler)
    logger.addHandler(f_handler)