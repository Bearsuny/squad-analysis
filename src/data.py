import os
import subprocess
import json
import requests
from tool.logger import Logger
from bs4 import BeautifulSoup

data_logger = Logger('data').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        data_logger.debug('%s: %s' % (func.__name__, ' '.join(args)))
        return func(*args, **kwargs)

    return wrapper


@decorator
def pull_dataset(url, path, file):
    '''wget the dataset from given url'''
    if not os.path.isdir(path):
        data_logger.info('%s %s %s' % (path, 'does not exist.', 'Build a new one.'))
        os.mkdir(path)
    if not os.path.isfile(os.path.join(path, file)):
        data_logger.info('%s %s %s' % (url.split('/')[-1], 'is not downloaded.', 'Start downloading...'))
        subprocess.call('wget -P %s %s' % (path, url), shell=True)
    else:
        data_logger.info('%s %s %s' % (url.split('/')[-1], 'is downloaded.', 'Stop downloading...'))


@decorator
def load_dataset(path, file):
    '''load the dataset from the given path and file'''
    with open(os.path.join(path, file), 'r') as file:
        return json.load(file)['data']


@decorator
def pull_l_data(url, path, file_s, file_d):
    '''wget the leaderboard data from given url and process the origin html in the form of json'''
    if not os.path.isdir(path):
        data_logger.info('%s %s %s' % (path, 'does not exist.', 'Build a new one.'))
        os.mkdir(path)
    if not os.path.isfile(os.path.join(path, file_s)):
        data_logger.info('%s %s %s' % (file_s, 'is not downloaded.', 'Start downloading...'))
        data = requests.get(url)
        with open(os.path.join(path, file_s), 'w') as f:
            f.write(data.text)
    else:
        data_logger.info('%s %s %s' % (file_s, 'is downloaded.', 'Stop downloading...'))
    with open(os.path.join(path, file_s), 'r') as f:
        data = f.read()
        s = BeautifulSoup(data, 'html.parser')
        result = []
        for tr in s.table.children:
            n = 0
            func = {
                '0': lambda x: x.string if x.p == None else x.p.string,
                '1': lambda x: ''.join(x.contents[0:1]),
                '2': lambda x: x.string,
                '3': lambda x: x.string
            }
            result_item = {}
            result_item_key = ['rank', 'model', 'em', 'f1']
            for item in tr.children:
                result_item[result_item_key[n % 4]] = func[str(n % 4)](item)
                n = n + 1
            result.append(result_item)
    with open(os.path.join(path, file_d), 'w') as f:
        json.dump(result, f)


@decorator
def load_l_data(path, file):
    '''load the leaderborad data from the given path and file'''
    with open(os.path.join(path, file), 'r') as file:
        return json.load(file)
