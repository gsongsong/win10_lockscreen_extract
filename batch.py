import configparser
import logging

from arrange import arrange
from extract import extract
from publish import publish
import util

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config')

    logfile = util.get_conf_logfile(config, default='log')
    loglevel = util.get_conf_loglevel(config, default=logging.DEBUG)

    logger = logging.getLogger(__file__)
    formatter = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s:'
                                  '%(lineno)d(%(funcName)s) %(msg)s')

    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    file_handler = logging.FileHandler(logfile)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    logger.setLevel(loglevel)

    logger.info('Starting win10_lockscreen_extract...')

    extract(config)
    arrange(config)
    publish(config)
