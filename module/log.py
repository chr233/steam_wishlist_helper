# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-06-21 15:46:23
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-07 18:03:15
# @Description  : 日志模块
'''

import logging
import os

debug = (os.getenv('mode', '').lower() == 'debug')

log_level = logging.DEBUG if debug else logging.INFO
log_format = '%(asctime)s [%(levelname)s] [%(name)s] %(message)s'
log_data = '%H:%M:%S'  # '%m-%d %H:%M:%S'

logging.basicConfig(level=log_level,
                    format=log_format,
                    datefmt=log_data)


def get_logger(tag: str = '-'):
    return (logging.getLogger(tag))