import json
import math
import numpy as np
import pandas as pd
import matplotlib as plt
from tool.logger import Logger

analysis_logger = Logger('analysis').get_logger()


def decorator(func):
    def wrapper(*args, **kwargs):
        analysis_logger.debug('%s: %s' % (func.__name__, 'data'))
        return func(*args, **kwargs)

    return wrapper


@decorator
def extract_info(data):
    '''extract the number of titles, paragraphs and questions'''
    t = len(data)

    p_t = np.zeros(t, dtype='int')
    for i in range(t):
        p_t[i] = len(data[i]['paragraphs'])
    p_t_pd = pd.DataFrame(data=p_t)

    q_p = np.zeros(p_t_pd.sum(), dtype='int')
    for i in range(t):
        for j in range(p_t[i]):
            q_p[j + sum(p_t[:i])] = len(data[i]['paragraphs'][j]['qas'])
    q_p_pd = pd.DataFrame(data=q_p)

    q_t = np.zeros(t, dtype='int')
    for i in range(t):
        q_t[i] = sum(q_p[sum(p_t[:i]):sum(p_t[:i + 1])])
