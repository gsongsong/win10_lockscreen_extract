import configparser
import git
import logging
import os
from PIL import Image
import util


def generate_thumbnails(thumb_path, img_path):
    if not os.path.isdir(thumb_path):
        os.mkdir(thumb_path)

    original_files = [f for f in os.listdir(img_path) if f.endswith('.jpg')]
    thumb_files = [f for f in os.listdir(thumb_path) if f.endswith('.jpg')]
    for fname in original_files:
        if fname in thumb_files:
            continue

        im = Image.open(img_path + fname)
        (x, y) = im.size
        h = 270
        w = x * h / y
        im.thumbnail((w, h), Image.ANTIALIAS)
        im.save(thumb_path + fname, 'JPEG')
        thumb_files += [fname]

    return [f for f in os.listdir(img_path) if f.endswith('.jpg')]


def generate_html(repo_path, thumb_files):
    html_file = open(repo_path + 'index.html', 'w')
    html_file.write('''
<html>
    <head>
        <title>Windows 10 Lockscreens</title>
        <script src="js/jquery-3.1.0.min.js"></script>
        <script src="js/jquery.lazyload.js"></script>
        <style>
            a {
                text-decoration: none;
            }
        </style>
    </head>
    <div style="text-align:center;">
        <h1>Windows 10 Lockscreens</h1>
        <ul style="list-style-type: none;">
''')
    cnt = 0
    for filename in thumb_files:
        if not cnt % 2:
            html_file.write('''
            <li>
''')

        if 'land' in filename:
            w = 480
        if 'port' in filename:
            w = 151
        html_file.write('''
                <a href=images/%s>
                    <img class=lazy data-original=thumbnails/%s width=%s height=270>
                </a>
''' % (filename, filename, w))

        if cnt % 2:
            html_file.write('''
            </li>
''')
        cnt += 1

    html_file.write('''
        </ul>
    </div>
    <script>
        $(function() {
            $('img.lazy').lazyload();
        });
    </script>
</html>
''')
    html_file.close()


def publish_repo(repo_path):
    repo = git.Repo(repo_path)
    repo.git.add('index.html')
    repo.git.add('images/')
    repo.git.add('thumbnails/')
    try:
        repo.git.commit('-m updated')
    except:
        exit()
    origin = repo.remote('origin')
    origin.push()


def publish(config: configparser.ConfigParser):
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

    logger.info('Publishing...')

    # TODO: need to check branch
    repo_path, branch = util.get_conf_repoinfo(config)
    img_path = util.get_conf_imgpath(config)
    thumb_path = util.get_conf_thumbpath(config)

    thumb_files = generate_thumbnails(thumb_path, img_path)
    generate_html(repo_path, thumb_files)
    publish_repo(repo_path)


if __name__ == "__main__":
    config = configparser.ConfigParser()
    config.read('config')

    publish(config=config)
