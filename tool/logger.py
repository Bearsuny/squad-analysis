import logging
import time
import os
import datetime
from tool.prjdir import get_prjdir


class Formatter(logging.Formatter):
    def formatTime(self, record, datefmt=None):
        ct = self.converter(record.created)
        if datefmt:
            s = time.strftime(datefmt, ct)
        else:
            s = str(datetime.datetime.now().strftime('%H:%M:%S:%f'))
        return s


class Logger(object):
    def __init__(self, name):
        # f1: format line one | f2: format line two | lf: log format
        f1 = '%(asctime)s %(filename)s %(levelname)s'
        f2 = '\n%(funcName)s %(lineno)s %(name)s'
        f3 = '\n%(message)s'
        f4 = '\n'
        lf = Formatter(f1 + f2 + f3 + f4, datefmt=None)

        # sh: stream handler
        sh = logging.StreamHandler()
        sh.setLevel(logging.DEBUG)
        sh.setFormatter(lf)

        # lp: log file path | ln: log file name | fh： file handler
        lp = os.path.join(get_prjdir(), 'log')
        if not os.path.isdir(lp):
            os.mkdir(lp)
        ln = time.strftime('%y-%m-%d', time.localtime(time.time())) + '.log'
        fn = os.path.join(lp, ln)

        fh = logging.FileHandler(filename=fn, mode='a', encoding='utf-8')
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(lf)

        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.DEBUG)
        self.logger.addHandler(sh)
        self.logger.addHandler(fh)

    def get_logger(self):
        return self.logger
