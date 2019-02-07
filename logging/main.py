import logging
from utils import config_logger, get_logger
from other import boo, goo

# log = logging.getLogger(__name__)
log = get_logger()

def main():
    config_logger()
    log.info('Start main')
    boo()
    goo()
    log.info('Finish main')

if __name__ == '__main__':
    main()
