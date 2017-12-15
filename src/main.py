import os
from tool.prjdir import *
from src.data import *
from src.analysis import *


def stage_1():
    url_list = ['https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json',
                'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json']

    for url in url_list:
        pull_dataset(url, os.path.join(get_prjdir(), 'data'), url.split('/')[-1])
        dataset = load_dataset(os.path.join(get_prjdir(), 'data'), url.split('/')[-1])
        dataset_info = extract_dataset_info(dataset)


def stage_2():
    pull_l_data('https://rajpurkar.github.io/SQuAD-explorer/', os.path.join(get_prjdir(), 'data'),
                'algorithm-rank.html', 'algorithm-rank.json')
    l_data = load_l_data(os.path.join(get_prjdir(), 'data'), 'algorithm-rank.json')
    l_s_data = extract_given_l_data(l_data, 'single')
    l_e_data = extract_given_l_data(l_data, 'ensemble')
    plot_l_data([l_s_data, l_e_data])


if __name__ == '__main__':
    # stage_1()
    stage_2()
