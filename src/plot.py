import os
import re
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tool.logger import Logger
from tool.prjdir import get_prjdir

plot_logger = Logger('plot').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        plot_logger.debug(func.__name__)
        return func(*args, **kwargs)

    return wrapper


@decorator
def plot_l_data(data):
    '''plot leaderboard data'''
    plt.figure(figsize=(20, 8))
    bar_width = 0.55
    name_list = ['single', 'ensemble']

    for i, item in enumerate(data):
        xaxis, xlabel, yaxis_1, yaxis_2 = [], [], [], []
        data_slice = item[0:10]
        xaxis = np.arange(len(data_slice) * 2)[::2]
        for item in data_slice:
            xlabel.append(strip_xlabel(item['model']))
            yaxis_1.append(float(item['em']))
            yaxis_2.append(float(item['f1']))

        ax = plt.subplot2grid((2, 1), (i, 0))
        ax.set_title('Leaderboard about SQuAD (%s model)' % name_list[i])
        ax.set_ylabel('Percentage (%)')
        ax.bar(xaxis, yaxis_1, bar_width, fc='w', ec='black')
        ax.bar(xaxis + bar_width, yaxis_2, bar_width, fc='w', ec='black', hatch='///')
        for x, y in zip(xaxis, yaxis_1):
            ax.text(x, y, '%.2f' % y, ha='center', va='bottom')
        for x, y in zip(xaxis, yaxis_2):
            ax.text(x + bar_width, y, '%.2f' % y, ha='center', va='bottom')
        plt.xticks(xaxis + bar_width / 2, xlabel)
        b_patch = mpatches.Rectangle((1, 1), 0, 0, fill=None, label='EM')
        r_patch = mpatches.Rectangle((1, 1), 0, 0, fill=None, label='F1', hatch='///')
        ax.legend(handles=[b_patch, r_patch], loc='upper right')
        ax.set_ylim(70, 100)

    plt.subplots_adjust(hspace=0.5)
    plt.savefig(os.path.join(get_prjdir(), 'output', 'l_data.jpg'))

    plot_logger.info('plot leaderborad data completed')


@decorator
def strip_xlabel(label):
    '''strip extra symbol in xlabel'''
    s = re.sub(r'\(.*?\)', '', label).replace('+', '')
    result = ''
    sum = 0
    for item in s.split():
        sum = sum + len(item)
        if sum > 15:
            result = '{}\n{}'.format(result, str(item))
            sum = 0
        else:
            result = '{} {}'.format(result, str(item))
    return result
