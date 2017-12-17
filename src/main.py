import os
from tool.prjdir import *
from src.data import *
from src.analysis import *
from src.plot import *


def stage_1():
    '''get train dataset and dev dataset, then extract the static describe'''
    url_list = ['https://rajpurkar.github.io/SQuAD-explorer/dataset/train-v1.1.json',
                'https://rajpurkar.github.io/SQuAD-explorer/dataset/dev-v1.1.json']

    dataset_describe = {}

    for url in url_list:
        pull_dataset(url, os.path.join(get_prjdir(), 'data'), url.split('/')[-1])
        dataset = load_dataset(os.path.join(get_prjdir(), 'data'), url.split('/')[-1])
        dataset_info = extract_dataset_info(dataset)
        name = '%s_dataset' % url.split('/')[-1].split('-')[0]
        dataset_describe[name] = dataset_info

    save_data(dataset_describe, os.path.join(get_prjdir(), 'output'), 'dataset_describe.json')


def stage_2():
    '''get leaderboard data and plot the top 5 model EM and F1'''
    pull_l_data('https://rajpurkar.github.io/SQuAD-explorer/', os.path.join(get_prjdir(), 'data'),
                'algorithm-rank.html', 'algorithm-rank.json')
    l_data = load_l_data(os.path.join(get_prjdir(), 'data'), 'algorithm-rank.json')
    l_s_data = extract_given_l_data(l_data, 'single')
    l_e_data = extract_given_l_data(l_data, 'ensemble')
    plot_l_data([l_s_data, l_e_data])


if __name__ == '__main__':
    stage_1()
    stage_2()
