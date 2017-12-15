import json
import math
import os
import re
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from tool.logger import Logger
from tool.prjdir import get_prjdir

analysis_logger = Logger('analysis').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        analysis_logger.debug('%s: %s' % (func.__name__, 'data'))
        return func(*args, **kwargs)

    return wrapper


@decorator
def extract_dataset_info(data):
    '''extract the number of titles, paragraphs and questions from origin data'''
    t = len(data)

    p_t = np.zeros(t, dtype='int')
    for i in range(t):
        p_t[i] = len(data[i]['paragraphs'])
    p_t_pd = pd.Series(data=p_t)
    analysis_logger.debug('%s:\n%s' % ('the number of p in t', p_t_pd.describe()))

    q_p = np.zeros(p_t_pd.sum(), dtype='int')
    for i in range(t):
        for j in range(p_t[i]):
            q_p[j + sum(p_t[:i])] = len(data[i]['paragraphs'][j]['qas'])
    q_p_pd = pd.Series(data=q_p)
    analysis_logger.debug('%s: %s' % ('the number of q in p', q_p_pd.describe()))

    q_t = np.zeros(t, dtype='int')
    for i in range(t):
        q_t[i] = sum(q_p[sum(p_t[:i]):sum(p_t[:i + 1])])
    q_t_pd = pd.Series(data=q_t)
    analysis_logger.debug('%s: %s' % ('the number of q in t', q_t_pd.describe()))

    return {'p_t_pd': p_t_pd, 'q_p_pd': q_p_pd, 'q_t_pd': q_t_pd}


@decorator
def plot_l_data(data):
    '''plot leaderboard data'''
    plt.figure(figsize=(10, 8))
    bar_width = 0.55
    name_list = ['single', 'ensemble']

    for i in range(len(data)):
        xaxis, xlabel, yaxis_1, yaxis_2 = [], [], [], []
        data_slice = data[i][0:5]
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
    plt.show()
    # plt.savefig(os.path.join(get_prjdir(), 'output', 'l_data.jpg'))


@decorator
def extract_given_l_data(data, name):
    '''extract the single and ensemble model seperately'''
    result = []
    result.append(data[-1])
    for item in data:
        if name in item['model']:
            result.append(item)
    return result


@decorator
def strip_xlabel(label):
    '''strip extra symbol in xlabel'''
    s = re.sub(r'\(.*?\)', '', label).replace('+', '')
    result = ''
    sum = 0
    for item in s.split():
        sum = sum + len(item)
        if sum > 15:
            result = result + '\n' + str(item)
            sum = 0
        else:
            result = result + ' ' + str(item)

    return result
