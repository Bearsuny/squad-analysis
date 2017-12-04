import os
import subprocess
from tool.logger import Logger

data_logger = Logger('data').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        data_logger.info('%s: %s' % (func.__name__, ' '.join(args)))
        return func(*args, *kwargs)

    return wrapper


@decorator
def pull_data(url, dir_path):
    if not os.path.isdir(dir_path):
        data_logger.info('%s %s %s' % (dir_path, 'does not exist.', 'Build a new one.'))
        os.mkdir(dir_path)
    if not os.path.isfile(os.path.join(dir_path, url.split('/')[-1])):
        data_logger.info('%s %s %s' % (url.split('/')[-1], 'is not downloaded.', 'Start downloading...'))
        subprocess.call('wget -P %s %s' % (dir_path, url), shell=True)
