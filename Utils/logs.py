import logging
import os

from logging.handlers import RotatingFileHandler
from datetime import datetime

dir_path = os.path.dirname(os.path.realpath(__file__))


def initialize_logger(output_dir):
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(levelname)-8.8s - %(asctime)s [%(filename)s][%(funcName)s]  %(message)s")

    # current time
    current_time = datetime.now().strftime('%Y%m%d')

    # create error file handler and set level to error
    handler = RotatingFileHandler(dir_path + "/log_files/" + current_time + "_error_" + output_dir + ".log",
                                  "a", maxBytes=10000000, backupCount=1, encoding=None, delay="true")
    handler.setLevel(logging.ERROR)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    # create debug file handler and set level to debug
    # handler = RotatingFileHandler(dir_path + "/log_files/" + current_time + "_debug_" + output_dir + ".log", "a",
    #                               maxBytes=10000000, backupCount=1)
    # handler.setLevel(logging.DEBUG)
    # handler.setFormatter(formatter)
    # logger.addHandler(handler)
