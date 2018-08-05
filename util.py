import configparser
import logging
import os
from pathlib import Path
import platform
import sys


def check_os(logger: logging.Logger):
    logger.info('Checking Windows 10...')

    err_msg = 'This system is not Windows 10. Exit.'
    if sys.platform != 'win32':
        raise OSError(err_msg)
    if platform.release() != '10':
        raise OSError(err_msg)


def get_conf_logfile(config: configparser.ConfigParser, default='log'):
    if config.has_section('Log'):
        if config.has_option('Log', 'file'):
            return config.get('Log', 'file')
    return default


def get_conf_loglevel(config: configparser.ConfigParser,
                      default=logging.WARNING):
    if config.has_section('Log'):
        if config.has_option('Log', 'level'):
            item = config.get('Log', 'level')
            if item.isdigit():
                return int(item)
    return default


def get_conf_repoinfo(config: configparser.ConfigParser):
    repopath = os.path.expanduser(config.get('Publish', 'path'))
    return Path(repopath), Path(config.get('Publish', 'branch'))


def get_conf_srcpath(config: configparser.ConfigParser):
    return Path(os.path.expanduser(config.get('Directory', 'src')))


def get_conf_imgpath(config: configparser.ConfigParser):
    return Path(os.path.expanduser(config.get('Publish', 'path'))) / 'images/'


def get_conf_thumbpath(config: configparser.ConfigParser):
    return Path(os.path.expanduser(config.get('Publish', 'path'))) / 'thumbnails/'
