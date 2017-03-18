import configparser
import git
import logging
import numpy as np
import os
from PIL import Image
import scipy.misc as misc
import shutil
import util


def initialize(repo_path, logger: logging.Logger):
    logger.info('Initializing directories...')

    if not os.path.isdir(repo_path):
        logger.info('{0} does not exists. Creating it...'.format(repo_path))
        os.mkdir(repo_path)

    if not os.path.isdir(repo_path + 'dups/'):
        logger.info('{0} does not exists. Creating it...'
                    .format(repo_path + 'dups/'))
        os.mkdir(repo_path + 'dups/')

    return repo_path


def get_extracted_files(dst_path, logger: logging.Logger):
    logger.info('Getting list of already extracted files...')

    published_files = [f for f in os.listdir(dst_path) if f.endswith('.jpg')]
    dup_files = [f for f in os.listdir(dst_path + 'dups/')if f.endswith('.jpg')]

    return published_files + dup_files


def already_extracted(filename, extracted_files, logger: logging.Logger):
    for c in extracted_files:
        if filename in c:
            return True

    return False


def extract_files(src_path, extracted_files, logger:logging.Logger):
    logger.info('Extracting new files...')

    list_files = os.listdir(src_path)
    list_land = []
    list_port = []
    for filename in list_files:
        if already_extracted(filename, extracted_files, logger):
            continue

        src_file = src_path + filename
        # check if it is image or not
        try:
            im = Image.open(src_file)
        except OSError:
            continue

        x, y = im.size
        im.close()
        if x == 1920 and y == 1080:
            list_land += [filename]
        if x == 1080 and y == 1920:
            list_port += [filename]

    return list_land, list_port


def build_differencematrix(src_path, list_land, list_port,
                           logger: logging.Logger):
    logger.info('Building difference matrix...')

    difference_matrix = []
    for land in list_land:
        im_land = np.array(Image.open(src_path + land))
        im_land = im_land[:, (960-304):(960+304), :]

        difference_row = []
        for port in list_port:
            im_port = np.array(Image.open(src_path + port))
            im_port = misc.imresize(im_port, (1080, 608))
            difference_row += [np.sum((im_land - im_port) ** 2) / (608 * 1080)]
        difference_matrix += [difference_row]

    return np.array(difference_matrix)


def copy_unique_filepairs(difference_matrix, src_path, list_land, list_port,
                          img_path,
                          logger: logging.Logger):
    logger.info('Copying new unique files...')

    cnt = 0
    while True:
        n = len(list_land)
        m = len(list_port)
        if not n:
            break

        arg_land, arg_port = np.unravel_index(np.argmin(difference_matrix), (n, m))

        logger.debug('  {0}'.format(list_land[arg_land]))
        logger.debug('  {0}'.format(list_port[arg_land]))
        logger.debug('    {0}'.format(list_land[arg_land] + 'XXXX' +
                                      list_port[arg_port] + '.jpg'))

        shutil.copyfile(src_path + list_land[arg_land],
                        img_path +
                        list_land[arg_land] + '-land-' +
                        list_port[arg_port] + '.jpg')
        shutil.copyfile(src_path + list_port[arg_port],
                        img_path +
                        list_land[arg_land] + '-port-' +
                        list_port[arg_port] + '.jpg')
        cnt += 1

        del list_land[arg_land], list_port[arg_port]
        difference_matrix = np.delete(difference_matrix, arg_land, 0)
        difference_matrix = np.delete(difference_matrix, arg_port, 1)

    logger.debug('{0} files copied'.format(cnt))


def extract(config: configparser.ConfigParser):
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

    util.check_os(logger=logger)

    logger.info('Extracting new files...')

    src_path = util.get_conf_srcpath(config)
    # TODO: need to check branch
    repo_path, branch = util.get_conf_repoinfo(config)
    img_path = util.get_conf_imgpath(config)
    initialize(repo_path, logger=logger)
    extracted_files = get_extracted_files(repo_path, logger=logger)
    list_land, list_port = extract_files(src_path, extracted_files,
                                         logger=logger)
    difference_matrix = build_differencematrix(src_path, list_land, list_port,
                                               logger=logger)
    copy_unique_filepairs(difference_matrix, src_path, list_land, list_port,
                          img_path,
                          logger=logger)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config')

    extract(config=config)
