# -*- coding: UTF-8 -*-
'''
# @Author       : Chr_
# @Date         : 2020-07-06 18:22:37
# @LastEditors  : Chr_
# @LastEditTime : 2020-11-26 16:00:05
# @Description  : 输出Json文件
'''
from json import dumps

from ..log import get_logger
from ..utils import get_output_path

logger = get_logger('Markdown')


def handler(wishdict: dict, index: list, symbol: str):
    '''
    这个函数将会被crawer调用

    参数:
        wishdict: 愿望单字典
    '''
    data = formater(wishdict, index, symbol)
    p = get_output_path('swh-json.json')
    with open(p, 'w+', encoding='utf-8') as f:
        f.write(data)
    logger.info(f'写入文件到 {p}')


def formater(wishdict: dict, index: list, symbol: str) -> str:
    '''
    这个函数用于从愿望单字典中提取数据

    参数:
        wishdict: 愿望单字典
    返回:
        str: 生成的结果
    '''    
    if wishdict:
        pass
    else:
        wishdict['error']=('游戏列表空,请检查过滤器设置以及是否将愿望单公开')
    return dumps(wishdict,ensure_ascii=False)
