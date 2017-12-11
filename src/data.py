import os
import subprocess
import json
from tool.logger import Logger

data_logger = Logger('data').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        data_logger.debug('%s: %s' % (func.__name__, ' '.join(args)))
        return func(*args, **kwargs)

    return wrapper


@decorator
def pull_data(url, data_path):
    '''wget the data from given url'''
    if not os.path.isdir(data_path):
        data_logger.info('%s %s %s' % (data_path, 'does not exist.', 'Build a new one.'))
        os.mkdir(data_path)
    if not os.path.isfile(os.path.join(data_path, url.split('/')[-1])):
        data_logger.info('%s %s %s' % (url.split('/')[-1], 'is not downloaded.', 'Start downloading...'))
        subprocess.call('wget -P %s %s' % (data_path, url), shell=True)


@decorator
def load_data(data_path):
    '''load data from the given data_path'''
    with open(data_path, 'r') as file:
        return json.load(file)['data']
