"""
AT-GSM-MODULE is a Python program that can send, receive and
manipulate AT commands via serial communication
"""

__title__ = 'at-gsm-module'
__version__ = '0.1'
__author__ = 'Seym, Samyo'

import logging
from gsmmodule.gsm import GSM

# logger
# ---------------------------
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# set logger format
logger_formatter = logging.Formatter(
    '(%(name)s) - %(levelname)s - %(message)s')

# create a console output handler
handler = logging.StreamHandler()
handler.setFormatter(logger_formatter)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)


logger.info(__title__)
logger.info('Version: ' + __version__)
logger.info('Authors: ' + __author__)
# ---------------------------
