import os
from tool.prjdir import get_prjdir
from src.data import pull_data

if __name__ == '__main__':
    url_list = ['https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json',
                'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json']
    for url in url_list:
        pull_data(url, os.path.join(get_prjdir(), 'data'))
