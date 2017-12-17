import numpy as np
import pandas as pd
from tool.logger import Logger

analysis_logger = Logger('analysis').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        analysis_logger.debug(func.__name__)
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

    q_p = np.zeros(p_t_pd.sum(), dtype='int')
    for i in range(t):
        for j in range(p_t[i]):
            q_p[j + sum(p_t[:i])] = len(data[i]['paragraphs'][j]['qas'])
    q_p_pd = pd.Series(data=q_p)

    q_t = np.zeros(t, dtype='int')
    for i in range(t):
        q_t[i] = sum(q_p[sum(p_t[:i]):sum(p_t[:i + 1])])
    q_t_pd = pd.Series(data=q_t)

    analysis_logger.info('extract dataset info completed')

    return {'p_t_pd': p_t_pd.describe().to_dict(), 'q_p_pd': q_p_pd.describe().to_dict(),
            'q_t_pd': q_t_pd.describe().to_dict()}


@decorator
def extract_given_l_data(data, name):
    '''extract the single and ensemble model seperately'''
    result = []
    result.append(data[-1])
    for item in data:
        if name in item['model']:
            result.append(item)

    analysis_logger.info('extract given %s data' % name)

    return result
