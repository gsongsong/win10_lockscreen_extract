import configparser
import git
import logging
import numpy as np
import os
from PIL import Image
import shutil
import util


def filter_list_with_keyword(item_list, keyword):
    return [i for i in item_list if keyword in i]


def get_staged_files(repo: git.Repo, logger):
    logger.info('Getting already staged files...')

    old_files = [e[0][7:] for e in repo.index.entries
                 if e[0].startswith('images/') and e[0].endswith('.jpg')]
    old_files_land = filter_list_with_keyword(old_files, 'land')
    old_files_port = filter_list_with_keyword(old_files, 'port')

    return old_files_land, old_files_port


def get_unstaged_files(repo: git.Repo, logger):
    logger.info('Getting unstaged files...')

    new_files = [f[7:] for f in repo.untracked_files
                 if f.startswith('images/') and f.endswith('.jpg')]
    new_files_land = filter_list_with_keyword(new_files, 'land')
    new_files_port = filter_list_with_keyword(new_files, 'port')

    return new_files_land, new_files_port


def cosine2d(m1: np.ndarray, m2: np.ndarray):
    dot_prod = np.sum(np.multiply(m1, m2))
    norm1 = np.sqrt(np.sum(m1 ** 2))
    norm2 = np.sqrt(np.sum(m2 ** 2))

    return dot_prod / norm1 / norm2


def build_confusionmatrix(img_path, unstaged_files, staged_files, logger):
    logger.info('Building confusion matrix...')

    entire_files = unstaged_files + staged_files
    n = len(unstaged_files)
    m = len(entire_files)

    confusion_matrix = np.zeros((n, m))
    confusion_matrix[:] = -1

    logger.debug('  {0} x {1} = {2} comparisons required, at maximum'
                 .format(n, m, n * m))
    for idx1, f1 in enumerate(unstaged_files):
        im1 = np.array(Image.open(img_path + f1)).astype(int) / 255
        for idx2, f2 in enumerate(entire_files):
            if idx2 <= idx1:
                continue
            im2 = np.array(Image.open(img_path + f2)).astype(int) / 255
            if im1.shape != im2.shape:
                continue

            confusion_matrix[idx1, idx2] = cosine2d(im1, im2)

    return confusion_matrix


def arrange_duplicates(img_path, unstaged_files_land, unstaged_files_port,
                       staged_files_land, staged_files_port,
                       confusion_matrix,
                       logger):
    entire_files_land = unstaged_files_land + staged_files_land
    entire_files_port = unstaged_files_port + staged_files_port

    for idx1, file_land1 in enumerate(unstaged_files_land):
        file_port1 = unstaged_files_port[idx1]

        n = np.argmax(confusion_matrix[idx1, :])
        file_land2 = entire_files_land[n]
        file_port2 = entire_files_port[n]

        if confusion_matrix[idx1, n] > 0.98:
            size1 = os.path.getsize(img_path + file_land1)
            size2 = os.path.getsize(img_path + file_land2)
            smaller_file_land, larger_file_land = (file_land1, file_land2)\
                if size1 < size2 else (file_land2, file_land1)
            smaller_file_port, larger_file_port = (file_port1, file_port2)\
                if size1 < size2 else (file_port2, file_port1)
            if smaller_file_land == larger_file_land:
                continue

            logger.debug('Duplicate')
            logger.debug('  Will be moved: {0}'.format(smaller_file_land))
            logger.debug('  Will remain  : {0}'.format(larger_file_land))
            logger.debug('  Will be moved: {0}'.format(smaller_file_port))
            logger.debug('  Will remain  : {0}'.format(larger_file_port))

            shutil.move(img_path + smaller_file_land,
                        img_path + 'dups/' + smaller_file_land)
            shutil.move(img_path + smaller_file_port,
                        img_path + 'dups/' + smaller_file_port)


def arrange(config):
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

    logger.info('Arranging files...')

    # TODO: need to check branch
    repo_path, branch = util.get_conf_repoinfo(config)
    img_path = util.get_conf_imgpath(config)
    repo = git.Repo(repo_path)

    staged_files_land, staged_files_port = get_staged_files(repo, logger)
    unstaged_files_land, unstaged_files_port = get_unstaged_files(repo, logger)
    confusion_matrix = build_confusionmatrix(img_path,
                                             unstaged_files_land,
                                             staged_files_land,
                                             logger)
    arrange_duplicates(img_path, unstaged_files_land, unstaged_files_port,
                       staged_files_land, staged_files_port,
                       confusion_matrix,
                       logger)

if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config')

    arrange(config=config)
